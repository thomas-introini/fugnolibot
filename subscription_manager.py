from pymongo import MongoClient

import logging as log
import time

client = MongoClient()
db = client['fugnolibot']


def get_active_subscriptions():
    return list(db['subscription'].find({'active': True}))


def get_subscription_by_user_id(user_id):
    return db['subscription'].find_one({'user_id': user_id, 'active': True})


def is_subscription_active(user_id):
    sub = get_subscription_by_user_id(user_id)
    return sub is not None


def insert_subscription(user_id, payload={}):
    db['subscription'].insert_one({
        'user_id': user_id,
        'active': True,
        'created_on': int(time.time()),
        'payload': payload,
        'last_nl_notified': None
    })


def update_last_nl_notified(user_id, date):
    try:
        result = db['subscription'].update_one(
            {
                'user_id': user_id,
                'active': True
            },
            {
                '$set': {
                    'last_nl_notified': date
                }
            }
        )
        return result.modified_count == 1
    except Exception as e:
        log.error(
            "Exception while updating last_nl_notified",
            e
        )
        return False


def deactivate_subscription(user_id):
    result = db['subscription'].update_one(
        {
            'user_id': user_id,
            'active': True
        },
        {
            '$set': {
                'active': False
            }
        }
    )
    return result.modified_count == 1
