import math


def fetch_avbl_balance(client, symbol: str):
    """
    사용가능한 잔고 조회 함수
    :param symbol: 'ETH' or 'USDT' or 'BTC' ...
    """
    balance = client.exchange.fetch_balance()
    avbl = math.floor(balance[symbol]["free"] * 100000000) / 100000000
    return avbl


def fetch_own_balances(client):
    """
    자산 조회
    """
    balances = client.exchange.fetch_balance()
    own_coin = [[i,j] for i,j in balances["total"].items() if j != 0.0]
    return own_coin


def fetch_latest_position(client, symbol: str):
    """
    최근 포지션 조회
    :param symbol: 'ETH/USDT' or 'BTC/USDT' or ...
    """
    orders = client.exchange.fetch_orders(symbol=symbol)
#    import pdb;pdb.set_trace();
    status = orders[-1]["info"]["status"]
    orderid = orders[-1]["id"]
    amount = orders[-1]["filled"]
    return status, orderid, amount


def fetch_pending(client, symbol: str):
    """
    미체결건 조회
    :param symbol: 'ETH', 'BTC', 'USDT', ...
    """
    orders = client.exchange.fetch_orders(symbol=symbol)
    latest_orderdata = orders[-1]["info"]
    status = latest_orderdata["status"]
    orderid = latest_orderdata["orderId"]

    pending = False
    if status == "NEW":
        pending = True
    return pending, orderid, status


def fetch_symbol(client, symbol: str, column: str) -> float:
    """
    당일 가격 조회
    :param symbol: 'ETH/USDT' or 'BTC/USDT', ...
    :param column: 'open', 'high', 'low', 'close'
    (close 는 최근 거래된 가격인 현재가격)
    :return: float type
    """
    price_info = client.exchange.fetch_ticker(symbol)
    return price_info[column]


def fetch_closed(client, symbol: str) -> str:
    """
    포지션 종료 여부 확인
    """
    orders = client.exchange.fetch_orders(symbol=symbol)
    status = orders[-1]["status"]
    return status
