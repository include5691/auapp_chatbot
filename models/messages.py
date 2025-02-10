from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(Integer, nullable=False)
    contact_id = Column(BigInteger)

    def __init__(self, timestamp: int, chat_id: int, message_id: int, contact_id: int):
        self.timestamp = timestamp
        self.chat_id = chat_id
        self.message_id = message_id
        self.contact_id = contact_id