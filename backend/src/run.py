#!/usr/bin/env python3

import cherrypy
import firebase_admin
import firebase_admin.messaging
import os

import logging

logger = logging.getLogger(__name__)


REG = {}


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    def register(self, token, name):
        print("REGISTER", token, name)
        REG[name] = token

    @cherrypy.expose
    def notify(self, name='hello'):
        token = REG.get(name, '')
        if not token:
            return 'NOT REGISTERED'
        msg = firebase_admin.messaging.MulticastMessage(
            data={'msg': 'notification msg'},
            webpush=firebase_admin.messaging.WebpushConfig(
                notification=firebase_admin.messaging.WebpushNotification('Ai meci', 'called', '/img/ball.png', image='/img/ball.png')
            ),
            tokens=[token]
        )
        response = firebase_admin.messaging.send_multicast(msg)
        print('Successfully sent message:', response)
        return 'ok'


def main():
    logging.basicConfig(level=logging.INFO)

    if not os.environ['GOOGLE_APPLICATION_CREDENTIALS']:
        print("GOOGLE_APPLICATION_CREDENTIALS must be set")
        exit(1)

    firebase_admin.initialize_app()

    conf = {
        '/': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            }
        }

    cherrypy.server.socket_host = '127.0.0.1'
    cherrypy.server.socket_port = 8088

    cherrypy.config.update({'environment': 'production'})
    cherrypy.quickstart(HelloWorld(), '/', conf)


if __name__ == '__main__':
    main()
