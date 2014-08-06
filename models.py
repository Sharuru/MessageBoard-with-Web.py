__author__ = 'Mave'

from web import db

#Database Object
database = db.database(dbn='sqlite', db='MessageRecord.db')


def select_table(table):
    return database.select(table)


def insert_in_msg(name, mail, time, message):
    return database.insert('msg', name=name, mail=mail, time=time, message=message)


def delete_in_msg(msgid):
    return database.delete('msg', where='msgid=$msgid', vars={'msgid': msgid})
