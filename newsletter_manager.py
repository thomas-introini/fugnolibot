from pymongo import MongoClient
from dateutil import parser
import logging as log

client = MongoClient()
db = client['fugnolibot']


def get_newsletters():
    return list(db['newsletters'].find())


def get_last_newsletter():
    c = db['newsletters'].find().sort('ts', -1).limit(1)
    return c[0] if c.count() >= 1 else None


def insert_newsletter(date, title, link):
    ts = int(parser.parse(date).timestamp())
    db['newsletters'].insert_one({
        'date': date,
        'ts': ts,
        'title': title,
        'link': link
    })
