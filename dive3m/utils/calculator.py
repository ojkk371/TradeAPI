import math


def cal_amount(symbol: str, price: float, avbl: float, ratio: float) -> float:
    """
    주문 수량 계산기
    :param symbol: 'USDT', 'BTC', ...
    :return: float
    """
    if symbol == "USDT":
        amount = math.floor(((avbl / price) * ratio) * 10000) / 10000
    else:
        amount = math.floor((avbl * ratio) * 10000) / 10000
    return amount


def truncate(num: float, n: int) -> float:
    """
    소수점 반올림 없이 버리기
    :param num: float
    :param n: n승
    :return: float type
    """
    number = int(num * (10**n))/(10**n)
    return float(number)


def cal_used_usdt(amount: float, price: float) -> float:
    """
    사용된 usdt 계산
    :param amount: float
    :param price: float
    """
    used_usdt = math.floor((amount * price) * 100000000) / 100000000
    return used_usdt
