import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.cors import CORSMiddleware
from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX
from app.database.conn import db, Base
from app.common.config import conf
from app.middlewares.token_validator import AccessControl
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from app.routes import index, auth, trade


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app():
    """
    앱 구성
    :return:
    """
    config = conf()
    app = FastAPI()

    db.init_app(app, **config)
    if not db.table_exist:
        Base.metadata.create_all(db.engine)

    app.add_middleware(
        AccessControl,
        except_path_list=EXCEPT_PATH_LIST,
        except_path_regex=EXCEPT_PATH_REGEX,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config["ALLOW_SITE"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=config["TRUSTED_HOSTS"],
        except_path=["/health"],
    )

    app.include_router(index.router)
    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
#    app.include_router(trade.router, tags=["Trade"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    app.include_router(trade.router, tags=["Trade"], prefix="/api")
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
