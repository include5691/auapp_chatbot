from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramContact(Base):
    "Customer map"
    __tablename__ = 'telegram_contacts'

    id = Column(BigInteger, primary_key=True) # contact id
    phone = Column(String(20))
    username = Column(String(128))
    timestamp = Column(Integer)

    def __init__(self, id: int, phone: str, username: str | None, timestamp: int):
        self.id = id
        self.phone = phone
        self.username = username
        self.timestamp = timestamp