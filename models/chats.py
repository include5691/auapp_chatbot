from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramChats(Base):
    "Customer map"
    __tablename__ = 'telegram_chats'

    id = Column(BigInteger, primary_key=True) # chat_id
    phone = Column(String)
    username = Column(String)

    timestamp = Column(Integer)
    user_id = Column(Integer) # bitrix user id

    def __init__(self, id: int, phone: str, username: str | None, timestamp: int, user_id: int):
        self.id = id
        self.phone = phone
        self.username = username
        self.timestamp = timestamp
        self.user_id = user_id