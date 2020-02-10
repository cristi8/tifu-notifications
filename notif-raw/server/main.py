#!/usr/bin/env python3

import os
import json
import logging

from flask import request, Response, render_template, jsonify, Flask
from pywebpush import webpush, WebPushException

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']


VAPID_PRIVATE_KEY = os.environ['VAPID_PRIVATE_KEY']
VAPID_PUBLIC_KEY = os.environ['VAPID_PUBLIC_KEY']

VAPID_CLAIMS = {
    "sub": "mailto:cristi8@gmail.com"
}


def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = request.get_json("subscription_token")
    return Response(status=201, mimetype="application/json")


@app.route("/push_v1/", methods=['POST'])
def push_v1():
    message = "Push Test v1"
    print("is_json", request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed': 1})

    print("request.json", request.json)

    token = request.json.get('sub_token')
    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success': 1})
    except Exception as e:
        print("error", e)
        return jsonify({'failed': str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
