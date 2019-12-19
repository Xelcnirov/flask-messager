import time
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
messages = [
    {'username': 'John', 'time': time.time(), 'text': 'Hello!'},
    {'username': 'Mary', 'time': time.time(), 'text': 'Hello, John!'},
]
password_storage = {
    'John': '12345',
    'Mary': '54321'
}

@app.route("/")
def hello_method():
    return "Hello, World!"

@app.route("/datetime")
def status_method():
    return str(datetime.now())

@app.route("/send", methods=['POST'])
def send_method():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    if username not in password_storage:
        password_storage[username] = password

    if not isinstance(username, str) or len(username) == 0:
        return {'ok': False}
    if not isinstance(text, str) or len(text) == 0:
        return {'ok': False}
    if password_storage[username] != password:
        return {'ok': False}

    messages.append(
        {'username': username,
        'time': time.time(),
        'text': text}
    )

    return {'ok': True}

@app.route("/messages")
def messages_method():

    after = float(request.args['after'])
    filtered_messages = [message for message in messages if message['time'] > after]

    return {'messages': filtered_messages}

app.run()
