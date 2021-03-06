#!/usr/bin/env python3

import os
import re
import logging
import io
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import cherrypy
import firebase_admin
import firebase_admin.messaging
import firebase_admin.firestore


logger = logging.getLogger(__name__)
Q = urllib.parse.quote_plus
with open(os.environ['TIFU_NOTIFY_SECRET'], 'r') as f:
    NOTIFY_SECRET = f.read().strip()


def clean_match_title(title: str):
    # Examples: 'OD Quali.: Qualification 3, Match 4', 'OD Pro 1/4', 'OD Semi 1/4'
    if title.startswith('OD Quali.: ') or title.startswith('OS Quali.: '):
        title = title[len('O? Quali.: '):]
    elif title.startswith('OD Semi ') or title.startswith('OS Semi '):
        title = title.replace('OD Semi ', 'SemiPro ').replace('OS Semi ', 'SemiPro ')
    elif title.startswith('OD Pro ') or title.startswith('OS Pro '):
        title = title[3:]
    elif title.startswith('M-DYP: '):
        title = title.replace('M-DYP: ', '')

    if 'Final' in title:
        title = '🥇 ' + title + ' 🥇'
    elif '3rd Place' in title:
        title = '🥉 ' + title + ' 🥉'

    return title


class TifuNotificationsBackend(object):
    def __init__(self):
        self.regex_called_d = re.compile(r'^(.*) \((.*) / (.*) versus (.*) / (.*)\) (called|started).$')
        self.regex_called_s = re.compile(r'^(.*) \(([^/]*) versus ([^/]*)\) (called|started).$')

    def _get_tokens_of(self, player_name, db):
        if not player_name:
            # Enforce opting out of notifications when choosing an empty name
            return []
        db_results = db.collection('reg').where('name', '==', player_name.lower()).limit(100).stream()
        return [db_doc.id for db_doc in db_results]

    @cherrypy.expose
    def register(self, token, name):
        logger.info("REGISTER as %s: %s", name, token)
        db = firebase_admin.firestore.client()
        db_doc = db.collection('reg').document(token)
        db_doc.set({'name': name.lower()})

    @cherrypy.expose
    def new_action(self, secret, action_str, table='-1', score=''):
        re_match = re.match(self.regex_called_d, action_str)
        if re_match:
            match_title, p11, p12, p21, p22, _ = re_match.groups()
            return self.match_called_d(secret, p11, p12, p21, p22, match_title, table=table)

        re_match = re.match(self.regex_called_s, action_str)
        if re_match:
            match_title, p1, p2, _ = re_match.groups()
            return self.match_called_s(secret, p1, p2, match_title, table=table)

        logger.warning("Unknown action: %s", action_str)
        return "unknown"

    @cherrypy.expose
    def match_called_d(self, secret, p11, p12, p21, p22, title='Test', table='-1'):
        table = int(table) + 1
        if secret != NOTIFY_SECRET:
            logger.error("BAD SECRET: '%s'", secret)
            return "denied"
        names = [p11, p12, p21, p22]
        teammates = [p12, p11, p22, p21]
        opponents = [[p21, p22], [p21, p22], [p11, p12], [p11, p12]]

        logger.info(f"Match called: {p11} / {p12} versus {p21} / {p22}")
        msgs = []
        db = firebase_admin.firestore.client()

        notif_title = 'Get ready'
        if table:
            notif_title += f' at table {table}'
        for i in range(4):
            name, teammate, opponent = names[i], teammates[i], opponents[i]
            name_tokens = self._get_tokens_of(name, db)
            for token in name_tokens:
                msg = firebase_admin.messaging.Message(
                    data={},
                    notification=firebase_admin.messaging.Notification(),
                    webpush=firebase_admin.messaging.WebpushConfig(
                        headers={
                            "Urgency": "high"
                        },
                        data={
                            'text_title': 'Get ready for ' + clean_match_title(title),
                            'text_body': f'You and {teammate} against {opponent[0]} and {opponent[1]}'
                        },
                        notification=firebase_admin.messaging.WebpushNotification(
                            title=notif_title,
                            body=clean_match_title(title),
                            icon='/img/icon.png?v=1',
                            badge="/img/badge.png",
                            image=f'/api/img?v=1.0&w=1024&h=325&p11={Q(p11)}&p12={Q(p12)}&p21={Q(p21)}&p22={Q(p22)}',
                            require_interaction=True,
                            tag='match_called',
                            renotify=True
                        )
                    ),
                    token=token
                )
                msgs.append(msg)
        firebase_admin.messaging.send_all(msgs)
        logger.info('Successfully sent %s notifications', len(msgs))
        return 'ok'

    @cherrypy.expose
    def match_called_s(self, secret, p1, p2, title='Test', table='-1'):
        table = int(table) + 1
        if secret != NOTIFY_SECRET:
            logger.error("BAD SECRET: '%s'", secret)
            return "denied"
        names = [p1, p2]
        opponents = [p2, p1]

        logger.info(f"Match called: {p1} versus {p2}")
        msgs = []
        db = firebase_admin.firestore.client()

        notif_title = 'Get ready'
        if table:
            notif_title += f' at table {table}'
        for i in range(2):
            name, opponent = names[i], opponents[i]
            name_tokens = self._get_tokens_of(name, db)
            for token in name_tokens:
                msg = firebase_admin.messaging.Message(
                    data={},
                    notification=firebase_admin.messaging.Notification(),
                    webpush=firebase_admin.messaging.WebpushConfig(
                        headers={
                            "Urgency": "high"
                        },
                        data={
                            'text_title': 'Get ready for ' + clean_match_title(title),
                            'text_body': f'You against {opponent}'
                        },
                        notification=firebase_admin.messaging.WebpushNotification(
                            title=notif_title,
                            body=clean_match_title(title),
                            icon='/img/icon.png?v=1',
                            badge="/img/badge.png",
                            image=f'/api/img?v=1.0&w=1024&h=325&p11={Q(p1)}&p21={Q(p2)}',
                            require_interaction=True,
                            tag='match_called',
                            renotify=True
                        )
                    ),
                    token=token
                )
                msgs.append(msg)
        firebase_admin.messaging.send_all(msgs)
        logger.info('Successfully sent %s notifications', len(msgs))
        return 'ok'

    @cherrypy.expose
    def img(self, p11, p21, p12="", p22="", w="720", h="240", v=''):
        w = int(w)
        h = int(h)
        if min(w, h) < 100 or max(w, h) > 2000:
            raise Exception("Invalid dimensions")
        img = Image.new('1', (w, h))
        draw = ImageDraw.Draw(img)

        if p12:
            team1 = f'{p11} / {p12}'
        else:
            team1 = p11
        if p22:
            team2 = f'{p21} / {p22}'
        else:
            team2 = p21
        versus = 'vs'

        font = None
        font_size = 64
        w_team1, w_team2, w_versus, h_team1, h_team2, h_versus = (0, 0, 0, 0, 0, 0)
        while font_size > 6:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=font_size)
            w_team1, h_team1 = draw.textsize(team1, font)
            w_versus, h_versus = draw.textsize(versus, font)
            w_team2, h_team2 = draw.textsize(team2, font)

            if max(w_team1, w_versus, w_team2) < 0.9 * w and h_team1 + 2 * h_versus + h_team2 < 0.9 * h:
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
    cherrypy.quickstart(TifuNotificationsBackend(), '/', conf)


if __name__ == '__main__':
    main()
