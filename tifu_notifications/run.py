#!/usr/bin/env python3
import json
import os, time, logging

import requests

from tifu_events import TifuEvents

logger = logging.getLogger(__name__)

PATH_SCRIPT = os.path.dirname(os.path.realpath(__file__))
PATH_TIFU = os.path.abspath(os.path.join(PATH_SCRIPT, '..'))
PATH_SECRET = os.path.join(PATH_SCRIPT, 'secret.txt')

with open(PATH_SECRET, 'r') as f:
    NOTIFY_SECRET = f.read().strip()
NOTIFY_URL = 'https://foos.cristi8.net/api/new_action'


def on_tifu_event(evt):
    logger.info("%s %s: %s", evt['tournament'], evt['type'], evt['info'])
    if evt['type'] == 'called':
        requests.post(NOTIFY_URL, {
            'secret': NOTIFY_SECRET,
            'action_str': evt['info']
        })


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("TiFu directory: %s", PATH_TIFU)
    tifu_events = TifuEvents(PATH_TIFU, on_tifu_event)
    tifu_events.start()


if __name__ == '__main__':
    main()
