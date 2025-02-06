from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramChat(Base):
    "Customer map"
    __tablename__ = 'telegram_chats'

    id = Column(BigInteger, primary_key=True) # chat_id
    phone = Column(String(20))
    username = Column(String(128))
    timestamp = Column(Integer)
    bitrix_user_id = Column(Integer)

    def __init__(self, id: int, phone: str, username: str | None, timestamp: int, bitrix_user_id: int):
        self.id = id
        self.phone = phone
        self.username = username
        self.timestamp = timestamp
        self.bitrix_user_id = bitrix_user_id