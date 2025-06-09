from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from core.db import Base

class Testing(Base):
    __tablename__='testing'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)


    