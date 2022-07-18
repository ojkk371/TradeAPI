from ..utils import Logger, split_ticker


def enter_limit_position(
    client,
    side: str,
    symbol: str,
    price: float,
    amount: float,
    leverage: int,
    isolated: bool,
    trade_type: str,
    test: bool = False,
):
    """
    포지션 진입 함수
    :param side: ex) 'buy' or 'sell'
    :param symbol: ex) 'BTC/USDT'
    :param price: 목표가(트레이딩뷰 신호 가격)
    :param amount: 수량
    :param leverage: 레버리지
    :param isolated: 마진모드, FALSE(cross) or TRUE(isolated)
    :param test: 테스트 유무
    """
    base, _ = split_ticker(symbol)

    client.leverage = leverage

    if isolated:
        margin_mode = str(isolated).upper()
        params = {"type": trade_type, "isIsolated": margin_mode, "test": test}
    else:
        params = {"type": trade_type, "test": test}

    try:
        response = client.exchange.create_order(
            symbol=symbol,
            type="limit",
            side=side,
            amount=amount,
            price=price,
            params=params
        )
        if response is not None:
            Logger.info(
                f"{side}:{symbol} 포지션 진입 요청 "
                f"Amount: {amount}({base}), Price: {price}({symbol})"
            )
        return response
    except Exception as e:
        Logger.error(f"{side} 포지션 진입 실패 - {e}")
        return False


def close_limit_position(
    client,
    side: str,
    symbol: str,
    price: float,
    amount: float,
    leverage: int,
    isolated: bool,
    trade_type: str,
    test: bool = False,
):
    """
    포지션 정리 함수
    :param side: ex) 'buy' or 'sell'
    :param symbol: ex) 'BTC/USDT'
    :param price: 목표가(트레이딩뷰 신호 가격)
    :param amount: 수량
    :param leverage: 레버리지
    :param isolated: 마진모드, FALSE(cross) or TRUE(isolated)
    :param test: 테스트 유무
    """
    base, _ = split_ticker(symbol)

    if side == "buy":
        side = "sell"
    else:
        side = "buy"
    try:
        response = enter_limit_position(
                client=client,
                side=side,
                symbol=symbol,
                price=price,
                amount=amount,
                leverage=leverage,
                isolated=isolated,
                trade_type=trade_type,
                test=test,
            )
        if response is not None:
            Logger.info(
                f"{side}:{symbol} 포지션 정리 요청 "
                f"Amount: {amount}({base}), Price: {price}({symbol})"
            )
        return response
    except Exception as e:
        Logger.error(f"{side} 포지션 정리 실패 - {e}")
        return False


def cancel_order(client, orderid: int, symbol: str):
    """
    주문취소
    :param orderid: 123412311
    :param symbol: ex) 'ETH/USDT' or 'BTC/USDT' ...
    """
    try:
        Logger.warning(f"미체결 주문 Symbol: {symbol}, Orderid: {orderid} 취소 요청")
        result = client.exchange.cancel_order(id=orderid, symbol=symbol)
        if result is not None:
            Logger.info(f"미체결 주문 Symbol: {symbol}, Orderid: {orderid} 취소 완료")
            return False
    except Exception as e:
        Logger.error(f"{orderid} an exception occured - {e}")
        return False
    return result
