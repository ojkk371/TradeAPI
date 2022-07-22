from pydantic import BaseModel
from os import path, environ


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


class Config(BaseModel):
    """
    General Configuration
    """

    BASE_DIR = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DB_URL: str = "mysql+pymysql://travis:1234@localhost:3306/trade_api?charset=utf8mb4"


class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


class TestConfig(Config):
    DB_URL: str = "mysql+pymysql://travis:1234@localhost:3306/trade_api?charset=utf8mb4"
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE = bool = True


def conf():
    """
    Load Config
    :return: dict
    """
    config = dict(prod=ProdConfig(), local=LocalConfig(), test=TestConfig())
    conf = config.get(environ.get("API_ENV", "local"))
    return conf.dict()
