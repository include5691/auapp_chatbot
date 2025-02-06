import time
from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramCommand(Base):
    __tablename__ = 'telegram_commands'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    command = Column(String)
    telegram_user_id = Column(BigInteger)

    def __init__(self, timestamp: int, command: str, telegram_user_id: int):
        self.command = command
        self.timestamp = timestamp
        self.telegram_user_id = telegram_user_id