from app.postgres_db import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import BIGINT


class Test(Base):
    __tablename__ = "eldorado_test"
    id = Column(BIGINT, primary_key=True, index=True)
    testfield = Column(String)
    newtestfield = Column(Integer)
    third_testfield = Column(Boolean)
