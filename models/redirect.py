import time
from sqlalchemy import Column, Integer, BigInteger, String
from _orm import Base

class TelegramRedirect(Base):
    __tablename__ = 'telegram_redirects'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    contact_id = Column(BigInteger)
    bitrix_user_id = Column(Integer)

    def __init__(self, contact_id: int, bitrix_user_id: int | None):
        self.timestamp = time.time()
        self.contact_id = contact_id
        self.bitrix_user_id = bitrix_user_id