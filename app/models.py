from enum import Enum
from pydantic import BaseModel
from pydantic.networks import EmailStr


# response model -> json
class TradingView(BaseModel):
    passphrase: str
    timestamp: str
    exchange: str
    ticker: str
    strategy: dict


# response model -> json
class UserRegister(BaseModel):
    email: EmailStr = None
    api_key: str = None
    secret_key: str = None


# incomming data
class Exchange(str, Enum):
    binance: str = "binance"
    upbit: str = "upbit"
    bithumb: str = "bithumb"


class TradeType(str, Enum):
    spot: str = "spot"
    margin: str = "margin"
    future: str = "future"


# response model -> json
class KeyPair(BaseModel):
    api_key: str = None
    secret_key: str = None


class TradeType(str, Enum):
    spot: str = "spot"
    margin: str = "margin"
    future: str = "future"


# response model -> json
class Token(BaseModel):
    Authorization: str = None


# object
class UserToken(BaseModel):
    email: str = None
    api_key: str = None
    secret_key: str = None
    exchange: str = None

    class Config:
        orm_mode = True
