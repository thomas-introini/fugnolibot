import logging as log
import urllib.request
import urllib.parse
import json
import os

TOKEN = os.getenv('FUGNOLI_BOT_TOKEN')

if not TOKEN:
    raise Exception("Token not set, Set it in the OS Environment")

BASE_URL = 'https://api.telegram.org/bot%s/' % TOKEN
OFFSET = -1


def set_offset(new_offset):
    global OFFSET
    OFFSET = new_offset


def get_updates():
    req = urllib.request.Request(
        url="%sgetUpdates?offset=%d" % (BASE_URL, OFFSET),
        data=None
    )
    with urllib.request.urlopen(req) as resp:
        updates = json.loads(resp.read().decode('utf-8'))
        if updates["ok"]:
            return updates["result"]
        else:
            raise Exception(
                "Error while getting updates: (%d) %s" %
                (updates["error_code"], updates["description"])
            )


def send_simple_message(chat_id, message):
    body = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    req = urllib.request.Request(
        method='POST',
        url=BASE_URL + 'sendMessage',
        data=urllib.parse.urlencode(body).encode()
    )
    with urllib.request.urlopen(req) as resp:
        jsonResponse = json.loads(resp.read().decode('utf-8'))
        log.info(jsonResponse)


def send_location(user_id, location):
    body = {
        'chat_id': user_id,
        'latitude': location["lat"],
        'longitude': location["lng"]
    }
    req = urllib.request.Request(
        method='POST',
        url=BASE_URL + 'sendLocation',
        data=urllib.parse.urlencode(body).encode()
    )
    with urllib.request.urlopen(req) as resp:
        jsonResponse = json.loads(resp.read().decode('utf-8'))
        if jsonResponse["ok"]:
            return jsonResponse["result"]
        else:
            raise Exception(
                "Error while sending message: (%d) %s" &
                (jsonResponse["error_code"], jsonResponse["description"])
            )


def request_location_message(user_id, message, keyboard_message):
    body = {
        'chat_id': user_id,
        'text': message,
        'reply_markup': {
            'keyboard': [
                [
                    {
                        'text': keyboard_message,
                        'request_location': True
                    }
                ]
            ],
            'one_time_keyboard': True,
            'resize_keyboard': True
        }
    }
    req = urllib.request.Request(
        method='POST',
        url=BASE_URL + 'sendMessage',
        data=json.dumps(body).encode(),
        headers={
            'Content-Type': 'application/json'
        }
    )
    with urllib.request.urlopen(req) as resp:
        jsonResponse = json.loads(resp.read().decode('utf-8'))
        if jsonResponse["ok"]:
            return jsonResponse["result"]
        else:
            raise Exception(
                "Error while sending message: (%d) %s" &
                (jsonResponse["error_code"], jsonResponse["description"])
            )
