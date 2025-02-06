from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramMap(Base):
    "Customer map"
    __tablename__ = 'telegram_map'

    id = Column(BigInteger, primary_key=True) # telegram user_id
    phone = Column(String(20))
    username = Column(String(128))
    timestamp = Column(Integer)

    def __init__(self, id: int, phone: str, username: str | None, timestamp: int):
        self.id = id
        self.phone = phone
        self.username = username
        self.timestamp = timestamp