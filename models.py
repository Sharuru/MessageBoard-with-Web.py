__author__ = 'Mave'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

#Database Object
engine = create_engine('mysql+mysqldb://username:password@localhost/database_name?charset=utf8')
Base = declarative_base()


class Msg(Base):
    __tablename__ = 'msg'
    msgid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    mail = Column(String(50))
    time = Column(String(50))
    message = Column(String(140))


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True)
    admin_name = Column(String(50), unique=True)
    admin_pass = Column(String(50))

Base.metadata.create_all(engine)
