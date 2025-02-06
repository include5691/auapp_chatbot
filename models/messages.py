from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(Integer, nullable=False)
    timestamp = Column(Integer)
    bitrix_user_id = Column(Integer)

    def __init__(self, chat_id: int, message_id: int, timestamp: int, bitrix_user_id: int | None):
        self.chat_id = chat_id
        self.message_id = message_id
        self.timestamp = timestamp
        self.bitrix_user_id = bitrix_user_id