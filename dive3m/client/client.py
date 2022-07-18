import ccxt
import yaml
from ..utils import Logger


class Client:
    """
    Description:
        A client-side representation of an Exchange account.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        trade_type: str = "future",
    ) -> None:
        """
        Args:
            trade_type: 'spot', 'margin' or 'future'
            private_file: Enter your config.yaml path
        """
        cls = type(self)
        self.__leverage = 1
        self.__margin_mode = "isolated"


        if trade_type is None:
            self.trade_type = trade_type
        else:
            self.trade_type = trade_type

        if not hasattr(cls, "_init"):
            self.client = ccxt.binance(
                {
                    "apiKey": api_key,
                    "secret": secret_key,
                    "enableRateLimit": True,
                    "options": {
                        "defaultType": self.trade_type,
                    },
                }
            )
            if self.trade_type != "spot":
                self.leverage = self.__leverage
                self.margin_mode = self.__margin_mode

    @property
    def exchange(self):
        return self.client

    @property
    def leverage(self):
        try:
            return self.__leverage
        except Exception as e:
            Logger.exception(e)

    @leverage.setter
    def leverage(self, leverage: int):
        """
        Args:
            leverage <= 50
            ticker: ex) 'ETH/USDT'
        """
        if leverage < 50:
            self.client.load_markets()
            res = self.client.set_leverage(leverage, "ETH/USDT")
            self.__leverage = int(res["leverage"])
            Logger.info(f"leverage: {self.__leverage}")
        else:
            raise ValueError("Enter a value less than 50")

    @property
    def margin_mode(self):
        if self.trade_type == "spot":
            print(f"trade_type '{self.trade_type}' does not support margin_mode.")
            Logger.error(
                f"trade_type '{self.trade_type}' does not support margin_mode."
            )
        else:
            try:
                return self.__margin_mode
            except Exception as e:
                print("ERR")

    @margin_mode.setter
    def margin_mode(self, marginmode: str):
        if self.trade_type != "spot":
            res = self.client.set_margin_mode(marginmode, "ETH/USDT")
            if res["code"] == "200" or "-4046":
                self.__margin_mode = marginmode
        else:
            print(f"trade_type '{self.trade_type}' does not support margin_mode.")
