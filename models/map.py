from sqlalchemy import Column, BigInteger, String
from _orm import Base

class TelegramMap(Base):
    "Customer map"
    __tablename__ = 'telegram_map'

    id = Column(BigInteger, primary_key=True)
    phone = Column(String)
    username = Column(String)

    def __init__(self, id: int, phone: str, username: str | None):
        self.id = id
        self.phone = phone
        self.username = username