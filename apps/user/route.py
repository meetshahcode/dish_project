
from fastapi import APIRouter, Depends, Response
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from apps.user import models, schema
from exceptions import UserAlreadyExistsException
from apps.user.jwt import set_tokens, get_current_user, SUB

router = APIRouter(tags=["User"],prefix="/auth")


@router.post("/register", response_model=schema.User)
async def register(
    data: schema.UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.
    """
    user = await models.User.find_by_email(db=db, email=data.email)
    if user:
        raise UserAlreadyExistsException()

    user_data = data.model_dump()
    user_data["password"] = models.get_password_hash(user_data["password"])

    user = models.User(**user_data)
    await user.save(db=db)

    user_schema = schema.User.model_validate(user.__dict__)
    return user_schema

@router.post("/login", response_model=schema.UserLoginResponse)
async def login(
    data: schema.UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """
    Login a user.
    """
    user = await models.User.authenticate(db=db, email=data.email, password=data.password)
    if not user:
        pass
    user_schema = schema.UserLoginResponse.model_validate(user.__dict__)
    set_tokens(user, response)
    return user_schema


@router.get("/me", response_model=schema.UserLoginResponse)
async def get_me(
    current_user: models.User = Depends(get_current_user),
):
    """
    Get the current user.
    """
    user_schema = schema.UserLoginResponse.model_validate(current_user.__dict__)
    return user_schema
