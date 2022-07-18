from app.common.consts import WEBHOOK_PASSPHRASE
from ..utils.formatting import reformat_ticker
import math


def parse_data(data: dict):
    """
    데이터 전처리
    :param data: dict
    """
    if data["passphrase"] != WEBHOOK_PASSPHRASE:
        return {"code": "error", "data": "passphrase is not correct"}
    else:
        side = data["strategy"]["order_action"]
        ticker = reformat_ticker(data["ticker"])
        price = math.floor((data["strategy"]["order_price"]) * 100000000) / 100000000
    return side, ticker, price

