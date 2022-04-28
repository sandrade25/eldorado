from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import BIGINT


class Test(Base):
    __tablename__ = "eldorado_test"
    id = Column(BIGINT, primary_key=True, index=True)
    testfield = Column(String)
    newtestfield = Column(Integer)