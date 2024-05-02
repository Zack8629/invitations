import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        extensions_list = ('.py', '.html', '.css', '.js', 'png', 'txt', 'ico')

        if event.is_directory or not event.src_path.endswith(extensions_list):
            return
        print(f'Detected change in {event.src_path}. Restarting Docker container.')
        subprocess.Popen(['docker-compose', 'up', '--build'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def start_watch(path_project='.'):
    print('Start of observation')

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path_project, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    start_watch()
