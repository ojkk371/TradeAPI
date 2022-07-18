from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from dive3m.client import Client
from dive3m.order.order import close_limit_position
from dive3m.utils import Logger, split_ticker, cal_amount, parse_data
from dive3m.order import enter_limit_position, cancel_order
from dive3m.fetcher import fetch_avbl_balance, fetch_latest_position
from app.models import TradeType, TradingView, KeyPair
from app.common.consts import API_KEY, SECRET_KEY
from dive3m.utils.calculator import truncate


router = APIRouter(prefix="/trade")


@router.post("/strategy/{strategy_name}")
async def trade(strategy_name: str, alert: TradingView, trade_type: str = "future", leverage: int = 1):
    """
    `거래 API`
    """
    client = Client(api_key=API_KEY, secret_key=SECRET_KEY, trade_type=trade_type)
    data = alert.dict()

    side, symbol, price = parse_data(data)
    _, quote = split_ticker(symbol)
    avbl = fetch_avbl_balance(client, quote)
    amount = cal_amount(symbol=quote, price=price, avbl=avbl, ratio=1)
    quantity = truncate(amount, 3)

    status, orderid, _ = fetch_latest_position(client, symbol)
    if status == "NEW":
        cancel_order(client, orderid, symbol)
        res = enter_limit_position(
                client=client,
                side=side,
                symbol=symbol,
                price=price,
                amount=quantity,
                leverage=leverage,
                trade_type=trade_type,
                isolated=True,
        )
    else:
        Logger.info("미체결건이 없습니다.")

    try:
        res = enter_limit_position(
                client=client,
                side=side,
                symbol=symbol,
                price=price,
                amount=quantity,
                leverage=leverage,
                trade_type=trade_type,
                isolated=True,
        )
        if res:
            Logger.info("포지션 진입 성공")
        else:
            Logger.warning("정리되지 않은 포지션이 있습니다.")
            _, _, amount = fetch_latest_position(client, symbol)
            quantity = truncate(amount, 3)
            res = enter_limit_position(
                    client=client,
                    side=side,
                    symbol=symbol,
                    price=price,
                    amount=quantity,
                    leverage=leverage,
                    trade_type=trade_type,
                    isolated=True,
            )
            if res:
                Logger.info(f"포지션 정리 성공")
            else:
                Logger.error(f"포지션 정리 실패")
            res = enter_limit_position(
                    client=client,
                    side=side,
                    symbol=symbol,
                    price=price,
                    amount=quantity,
                    leverage=leverage,
                    trade_type=trade_type,
                    isolated=True,
            )
            Logger.info(f"포지션 진입 성공 : {res}")
    except Exception as e:
        Logger.error(f"Exception : {e}")
    return JSONResponse(status_code=200, content=dict(data))
