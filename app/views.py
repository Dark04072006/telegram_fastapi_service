from . import schemas, auth
from sqlalchemy.orm import Session

from fastapi.routing import APIRouter
from fastapi import Depends

from .database import get_db

from . import crud
from .auth import JWTBearer
from .services import check_admin

api = APIRouter(prefix='/api/v1/users')


@api.post('/login', tags=['auth'])
def login(user: schemas.LoginSchema) -> dict:
    if check_admin(user.username, user.password):
        return auth.sign_jwt(user.username)
    return {'error': 'wrong login data'}


@api.get('/', response_model=list[schemas.UserSchema], dependencies=[Depends(JWTBearer())], tags=['users'])
def get_user_list(db: Session = Depends(get_db)) -> list[schemas.UserSchema]:
    return crud.get_users(db)


@api.post('/', response_model=schemas.UserSchema, dependencies=[Depends(JWTBearer())], tags=['users'])
def add_user(user: schemas.UserSchema, db: Session = Depends(get_db)) -> schemas.UserSchema:
    return crud.create_user(db, user)


@api.get('/{user_id}', dependencies=[Depends(JWTBearer())], tags=['users'])
def get_user_cur(user_id: int, db: Session = Depends(get_db)) -> schemas.UserSchema:
    return crud.get_user(db, user_id)


@api.get('/{user_id}/messages', dependencies=[Depends(JWTBearer())], tags=['messages'])
def get_msg_list(user_id: int, db: Session = Depends(get_db)) -> list[schemas.UserSchema]:
    return crud.get_user_messages(db, user_id)


@api.post('/{user_id}/messages', dependencies=[Depends(JWTBearer())], tags=['messages'])
def add_message(
        user_id: int,
        message: schemas.MessageSchema,
        db: Session = Depends(get_db)) -> list[schemas.MessageSchema]:
    return crud.add_user_messages(
        db,
        user_id,
        message
    )


@api.delete('/{user_id}/messages', tags=['messages'], dependencies=[Depends(JWTBearer())])
def delete_messages(
        user_id: int,
        db: Session = Depends(get_db)
    ) -> dict[str, int | str]:
    return crud.delete_messages(db, user_id)


@api.delete('/{user_id}', tags=['users'], dependencies=[Depends(JWTBearer())])
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
    ) -> dict[str, int | str]:
    return crud.delete_user(db, user_id)


@api.put('/{user_id}', tags=['users'], dependencies=[Depends(JWTBearer())])
def update_sub(
        user_id: int,
        user: schemas.UserUpdateSchema,
        db: Session = Depends(get_db),
    ):
    return crud.update_user(db, user_id, user)
