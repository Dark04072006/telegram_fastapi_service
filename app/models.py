import json

from sqlalchemy import Column, Integer, TEXT, Boolean
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    messages = Column(TEXT, default='[]')
    is_subscriber = Column(Boolean, default=False)

    def to_json(self):
        return {
            'user_id': self.user_id,
            'messages': json.loads(self.messages),
            'is_subscriber': self.is_subscriber
        }
