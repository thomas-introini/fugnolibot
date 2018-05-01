from pymongo import MongoClient
from dateutil import parser

client = MongoClient()
db = client['fugnolibot']


def get_newsletters():
    return list(db['newsletters'].find())


def get_last_newsletter():
    return db['newsletters'].find().sort('ts', -1).limit(1)


def insert_newsletter(date, title, link):
    ts = int(parser.parse(date).timestamp())
    db['newsletters'].insert_one({
        'date': date,
        'ts': ts,
        'title': title,
        'link': link
    })
