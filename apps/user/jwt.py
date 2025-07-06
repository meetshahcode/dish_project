import uuid
import sys
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends


from jose import jwt, JWTError
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings

from apps.user.models import User 
from apps.user.schema import JwtTokenSchema
from database import get_db
from exceptions import AuthFailedException
from apps.user.models import BlackListToken

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"

def _get_utc_now():
    return datetime.now(timezone.utc)

def _create_access_token(payload: dict, minutes: int = 0) -> JwtTokenSchema:
    expire = _get_utc_now() + timedelta(
        minutes = minutes if minutes else get_settings().access_token_expires_minutes
    )

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload, get_settings().secret_key, algorithm=get_settings().algorithm),
        payload=payload,
        expire=expire,
    )

    return token


def _create_refresh_token(payload: dict) -> JwtTokenSchema:
    expire = _get_utc_now() + timedelta(minutes=get_settings().refresh_token_expires_minutes)

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload, get_settings().secret_key, algorithm=get_settings().algorithm),
        expire=expire,
        payload=payload,
    )

    return token


def set_tokens(user: User, response: Response):
    payload = {SUB: str(user.id), JTI: str(uuid.uuid4()), IAT: _get_utc_now()}
    token = _create_access_token(payload={**payload}).token
    refresh = _create_refresh_token(payload={**payload}).token
    response.headers[get_settings().access_header] = token
    response.headers[get_settings().refresh_header] = refresh
    return

async def decode_access_token(token: str, db: AsyncSession):
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        black_list_token = await BlackListToken.find_by_id(db=db, id=payload[JTI])
        if black_list_token:
            raise JWTError("Token is blacklisted")
    except JWTError:
        raise AuthFailedException()

    return payload

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)) -> User:
    payload = await decode_access_token(db=db, token=token)
    user = await User.find_by_id(db=db, id=int(payload[SUB]))
    if not user:
        raise AuthFailedException("User not found")
    return user