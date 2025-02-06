import time
from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramCommand(Base):
    __tablename__ = 'telegram_commands'
    
    id = Column(Integer, primary_key=True)
    command = Column(String)
    timestamp = Column(Integer)
    bitrix_user_id = Column(Integer)

    def __init__(self, chat_id: int, message_id: int):
        self.chat_id = chat_id
        self.message_id = message_id
        self.timestamp = time.time()