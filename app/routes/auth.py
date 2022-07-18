from datetime import datetime, timedelta
import bcrypt, jwt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.common.consts import JWT_SECRET, JWT_ALGORITHM
from app.database.conn import db
from app.database.schema import Users
from app.models import Exchange, UserRegister, Token, UserToken


router = APIRouter(prefix="/auth")


@router.post("/register/{exchange}", status_code=200, response_model=Token)
async def register(exchange: Exchange, reg_info: UserRegister, session: Session = Depends(db.session)):
    """
    `회원가입 API`
    """
    if exchange == Exchange.binance:
        is_exist = await is_apikey_exist(reg_info.api_key)
        if not reg_info.api_key or not reg_info.secret_key or not reg_info.email:
            return JSONResponse(status_code=400, content=dict(msg="Api-key, Secret-Key and Email must be provided"))
        if is_exist:
            return JSONResponse(status_code=400, content=dict(msg=f"{exchange} Account EXISTS"))
        hash_secret_key = bcrypt.hashpw(reg_info.secret_key.encode("utf-8"), bcrypt.gensalt())
        new_user = Users.create(session, auto_commit=True, secret_key=hash_secret_key, api_key=reg_info.api_key, email=reg_info.email)
        token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'secret_key'}),)}")
        return token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


@router.post("/login/{exchange}", status_code=200, response_model=Token)
async def login(exchange: Exchange, user_info: UserRegister):
    """
    `로그인 API`
    """
    if exchange == Exchange.binance:
        is_exist = await is_apikey_exist(user_info.api_key)
        if not user_info.api_key or not user_info.secret_key or not user_info.email:
            return JSONResponse(status_code=400, content=dict(msg="Api-key and Secret-Key must be provided"))
        if not is_exist:
            return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        user = Users.get(api_key=user_info.api_key)
        is_verified = bcrypt.checkpw(user_info.secret_key.encode("utf-8"), user.secret_key.encode("utf-8"))
        if not is_verified:
            return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'secret_key'}),)}")
        return token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


async def is_apikey_exist(api_key: str):
    get_key = Users.get(api_key=api_key)
    if get_key:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
