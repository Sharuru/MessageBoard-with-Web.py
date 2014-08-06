__author__ = 'Mave'

from web import db

#Database Object
database = db.database(dbn='sqlite', db='MessageRecord.db')


def get_all_comments():
    return database.select('msg')