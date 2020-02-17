#!/usr/bin/env python3

import os, time, logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logger = logging.getLogger(__name__)

PATH_SCRIPT = os.path.dirname(os.path.realpath(__file__))
PATH_LOG = os.path.abspath(os.path.join(PATH_SCRIPT, '..', 'log'))
PATH_SECRET = os.path.join(PATH_SCRIPT, 'secret.txt')

with open(PATH_SECRET, 'r') as f:
    NOTIFY_SECRET = f.read().strip()


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("LOG directory: %s", PATH_LOG)

    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, PATH_LOG, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
