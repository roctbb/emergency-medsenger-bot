import datetime
import time
from threading import Thread
from flask import Flask, request, render_template
import json
import requests
import hashlib, uuid
from config import *
import threading
import csv
import json

app = Flask(__name__)

situations = [
    {
        "words": "кровотечение",
        "text": "В случае массивных кровотечений следует немедленно вызвать Скорую помощь, не дожидаясь ответа врача."
    },
    {
        "words": "обморок,потеря сознания",
        "text": "В случае обморока или потери сознания срочно вызовите Скорую помощь, не дожидаясь ответа врача."
    },
    {
        "words": "удушье,затрудненное дыхание",
        "text": "В случае удушья или затрудненного дыхания, срочно вызовите Скорую помощь, не ожидаясь ответа врача.  "
    },
    {
        "words": "одышка",
        "text": "В случае возникновения тяжелой одышки, не связанной с физической активностью, необходимо срочно вызвать Скорую помощь. Это может быть признаком серьезного заболевания."
    },
    {
        "words": "судороги,конвульсии",
        "text": "В случае возникновения судорог или конвульсий срочно вызовите Скорую помощь, не дожидаясь ответа врача."
    },
    {
        "words": "острая боль,резкая боль,сильная боль",
        "text": "В случае неожиданного возникновения резкой боли в груди, животе, голове или пояснице, срочно вызовите Скорую помощь, не дожидаясь ответа врача."
    },
]


def delayed(delay, f, args):
    timer = threading.Timer(delay, f, args=args)
    timer.start()


@app.route('/init', methods=['POST', 'GET'])
def init():
    return 'ok'


@app.route('/remove', methods=['POST'])
def remove():
    return 'ok'


@app.route('/settings', methods=['GET'])
def settings():
    return "<strong>Данный интеллектуальный агент не требует настройки.</strong>"


@app.route('/', methods=['GET'])
def index():
    return 'waiting for the thunder!'


def send_warning(contract_id, text):
    data = {
        "contract_id": contract_id,
        "api_key": APP_KEY,
        "message": {
            "text": text,
            "is_urgent": True,
        }
    }
    try:
        print('sending warning')
        result = requests.post(MAIN_HOST + '/api/agents/message', json=data)
    except Exception as e:
        print('connection error', e)


@app.route('/message', methods=['POST'])
def save_message():
    data = request.json
    key = data['api_key']
    contract_id = str(data['contract_id'])

    if key != APP_KEY:
        print("wrong key", key, "!=", APP_KEY)
        return "<strong>Некорректный ключ доступа.</strong> Свяжитесь с технической поддержкой."

    text = data['message']['text'].replace('\n', ' ').lower()
    print("Text:", text)

    for situation in situations:
        words = situation['words'].split(',')
        print("words", words)

        for word in words:
            if word in text:
                print("sending warning")
                delayed(1, send_warning, [contract_id, situation["text"]])
                break

    return "ok"


if not DEBUG:
    app.run(port='9093', host='0.0.0.0', ssl_context=SSL)
else:
    app.run(port='9093', host='0.0.0.0')
