#!/usr/bin/env python3

import cherrypy
import firebase_admin
import firebase_admin.messaging
import os
import urllib.parse

import logging
from PIL import Image, ImageDraw, ImageFont
import io


logger = logging.getLogger(__name__)


REG = {}

def get_tokens_of(player_name):
    if player_name not in REG:
        return []
    return [REG[player_name]]


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    def register(self, token, name):
        print("REGISTER", token, name)
        REG[name] = token

    @cherrypy.expose
    def notify(self, match):
        team1, team2 = match.split(' versus ')
        p11, p12 = team1.split(' / ')
        p21, p22 = team2.split(' / ')

        names = [p11, p12, p21, p22]
        teammates = [p12, p11, p22, p21]
        opponents = [[p21, p22], [p21, p22], [p11, p12], [p11, p12]]

        logger.info("Notifying match %s", match)
        msgs = []

        for i in range(4):
            name, teammate, opponent = names[i], teammates[i], opponents[i]
            name_tokens = get_tokens_of(name)
            for token in name_tokens:
                msg = firebase_admin.messaging.Message(
                    data={},
                    notification=firebase_admin.messaging.Notification(),
                    webpush=firebase_admin.messaging.WebpushConfig(
                        notification=firebase_admin.messaging.WebpushNotification(
                            title='Get ready',
                            body=f'Your match was called (vs {opponent[0]} and {opponent[1]})',
                            icon='/img/icon.png?v=1',
                            badge="/img/badge.png",
                            image='/api/img?w=1024&h=325&title=' + urllib.parse.quote_plus(match),
                            require_interaction=True
                        )
                    ),
                    token=token
                )
                msgs.append(msg)
        firebase_admin.messaging.send_all(msgs)
        logger.info('Successfully sent %s notifications', len(msgs))
        return 'ok'

    @cherrypy.expose
    def img(self, title, w="720", h="240"):
        w = int(w)
        h = int(h)
        if min(w, h) < 100 or max(w, h) > 2000:
            raise Exception("Invalid dimensions")
        img = Image.new('1', (w, h))
        draw = ImageDraw.Draw(img)

        team1, team2 = title.split(' versus ')
        versus = 'vs'

        font = None
        font_size = 64
        w_team1, w_team2, w_versus, h_team1, h_team2, h_versus = (0, 0, 0, 0, 0, 0)
        while font_size > 6:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=font_size)
            w_team1, h_team1 = draw.textsize(team1, font)
            w_versus, h_versus = draw.textsize(versus, font)
            w_team2, h_team2 = draw.textsize(team2, font)

            if max(w_team1, w_versus, w_team2) < w and h_team1 + 2 * h_versus + h_team2 < h:
                break
            font_size -= 1

        draw.text(((w - w_team1) // 2, (h - h_versus) // 2 - h_versus // 2 - h_team1), team1, fill='white', font=font)
        draw.text(((w - w_versus) // 2, (h - h_versus) // 2), versus, fill='white', font=font)
        draw.text(((w - w_team2) // 2, (h - h_versus) // 2 + h_versus // 2 + h_team2), team2, fill='white', font=font)

        cherrypy.response.headers['Content-Type'] = "image/png"
        output = io.BytesIO()
        img.save(output, 'PNG')
        contents = output.getvalue()
        output.close()
        return contents


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
