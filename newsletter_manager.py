from pymongo import MongoClient
from dateutil import parser
from typing import Dict, List

client = MongoClient()
db = client['fugnolibot']


def get_newsletters() -> List[Dict]:
    return list(db['newsletters'].find())


def get_last_newsletter() -> Dict:
    c = db['newsletters'].find().sort('ts', -1).limit(1)
    return c[0] if c.count() == 1 else None


def insert_newsletter(date: str, title: str, link: str) -> None:
    ts = int(parser.parse(date).timestamp())
    db['newsletters'].insert_one({
        'date': date,
        'ts': ts,
        'title': title,
        'link': link
    })
