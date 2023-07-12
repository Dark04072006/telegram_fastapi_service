import json

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(user_id=user_id).first().to_json()


def get_users(db: Session):
    return [user.to_json() for user in db.query(models.User).all()]


def create_user(db: Session, user: schemas.UserSchema):
    usr = db.query(models.User).filter_by(user_id=user.user_id).first()
    if usr is None:
        db_user = models.User(
            user_id=user.user_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.to_json()
    return usr.to_json()


def get_user_messages(db: Session, user_id: int):
    user = db.query(models.User).filter_by(user_id=user_id).first()
    if user is not None:
        return json.loads(user.messages)
    return {'message': 'user not found'}, 400


def add_user_messages(db: Session, user_id: int, messages: schemas.MessageSchema):
    user = db.query(models.User).filter_by(user_id=user_id).first()
    if user is not None:
        user_messages: list = json.loads(user.messages)
        user_messages.append({
            'role': messages.role,
            'content': messages.content
        })
        user.messages = json.dumps(user_messages)
        db.commit()
        return user.to_json()['messages']
    return {'message': 'user not found'}, 400


def delete_messages(db: Session, user_id: int):
    user = db.query(models.User).filter_by(user_id=user_id).first()
    if user is not None:
        user.messages = '[]'
        db.commit()
        return {'status': 204}
    return {'message': 'user not found'}, 400


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter_by(user_id=user_id).first()
    if user is not None:
        db.delete(user)
        db.commit()
        return {'status': 204}
    return {'message': 'user not found'}, 400


def update_user(db: Session, user_id: int, user: schemas.UserUpdateSchema):
    usr = db.query(models.User).filter_by(user_id=user_id).first()
    if usr is not None:
        db.query(models.User).filter_by(user_id=user_id).update({
            'is_subscriber': user.is_subscriber
        })
        db.commit()
        return 200
    return {'message': 'user not found'}, 400
