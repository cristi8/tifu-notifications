
import os, re, time, logging
import watchdog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

logger = logging.getLogger(__name__)


# This only works for files that are only appended to and all lines are different.
# In this case, there's a timestamp in each line
class NewLinesEventHandler(PatternMatchingEventHandler):
    def __init__(self, file_patterns, cb):
        super().__init__(file_patterns)
        self.new_lines_callback = cb
        self.seen_lines = {}

    def on_modified(self, event):
        try:
            self._on_file_modified(event)
        except Exception as ex:
            logger.error("Error processing file %s: %s", event.src_path, str(ex))

    def _on_file_modified(self, event):
        if event.src_path not in self.seen_lines:
            # Init with existing lines (except last line, which was actually modified)
            with open(event.src_path, 'r') as f:
                ignored_lines = f.read().splitlines(True)[:-1]
            self.seen_lines[event.src_path] = set(ignored_lines)

        with open(event.src_path, 'r') as f:
            lines = f.read().splitlines(True)
        full_lines = [line for line in lines if line and line[-1] in '\r\n']
        new_lines = [line for line in full_lines if line not in self.seen_lines[event.src_path]]

        for line in new_lines:
            self.seen_lines[event.src_path].add(line)
            try:
                self.new_lines_callback(event.src_path, line.strip())
            except Exception as ex:
                logger.error("Error handling line %s: %s", line.strip(), str(ex))


class TifuEvents(object):
    def __init__(self, tifu_installation_directory, callback):
        self.tifu_installation_directory = tifu_installation_directory
        self.callback = callback

    def _status_fpath_to_tournament_id(self, status_fpath):
        path_regex = r'.*[\\/]backup[\\/](.*)[\\/]Status_.*'
        re_match = re.match(path_regex, status_fpath)
        if not re_match:
            logger.error("Unexpected path: %s", status_fpath)
            return 'unknown'
        return re_match.groups()[0]

    def on_status_line(self, fpath, line):
        tournament_id = self._status_fpath_to_tournament_id(fpath)
        fields = line.split('###')
        if len(fields) < 2:
            logger.warning('Unexpected line in file %s: %s', fpath, line)
        evt = {
            'tournament': tournament_id,
            'raw': fields,
            'ts': fields[0],
            'itype': int(fields[2]),
            'type': {
                0: 'started',
                1: 'finished',
                2: 'called',
                3: 'unprotected',
                30: 'file_status_saved',
                40: 'recall'
            }.get(int(fields[2]), f'unknown ({fields[2]})'),
            'info': fields[-1]
        }
        self.callback(evt)

    def start(self):
        event_handler = NewLinesEventHandler([r'*\Status_*'], self.on_status_line)
        observer = Observer()
        observer.schedule(event_handler, os.path.join(self.tifu_installation_directory, 'backup'), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Ctrl+C was pressed. Closing...")
            observer.stop()
        observer.join()
