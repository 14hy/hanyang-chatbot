from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from datetime import datetime
from utils import KST


class Query(Base):
    """사용자 질문
    """
    __tablename__ = 'query'
    id = Column('id', Integer, primary_key=True)
    query = Column('query', String(50), nullable=False)
    added_time = Column('added_time', DateTime(timezone=True), nullable=False, default=datetime.now(tz=KST))

    def __init__(self):
        pass

    def __repr__(self):
        return None
