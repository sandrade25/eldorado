from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import BIGINT


class Test(Base):
    __tablename__ = "eldorado_test"
    id = Column(BIGINT, primary_key=True, index=True)
    testfield = Column(String)
    newtestfield = Column(Integer)
    third_testfield = Column(Boolean)