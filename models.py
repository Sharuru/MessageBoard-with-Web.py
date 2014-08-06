__author__ = 'Mave'

from web import db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

#Database Object
database = db.database(dbn='sqlite', db='MessageRecord.db')
engine = create_engine('sqlite:///MessageRecordv2.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Msg(Base):
    __tablename__ = 'msg'
    msgid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    mail = Column(String)
    time = Column(String)
    message = Column(String)


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True)
    admin_name = Column(String, unique=True)
    admin_pass = Column(String)


Base.metadata.create_all(engine)


def insert_in_msg(name, mail, time, message):
    new_msg = Msg(name=name, mail=mail, time=time, message=message)
    session.add(new_msg)
    session.commit()
    #return database.insert('msg', name=name, mail=mail, time=time, message=message)
    return True


def delete_in_msg(msgid):
    msgggg = Msg(msgid=msgid)
    session.delete(msgggg)
    return True
    #return database.delete('msg', where='msgid=$msgid', vars={'msgid': msgid})
