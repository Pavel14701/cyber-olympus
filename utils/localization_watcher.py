import os
import multiprocessing
import itertools
import time
import subprocess
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from path_getter import PathGetter
from dotenv import load_dotenv

class LocalizationHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.po'):
            po_file = event.src_path
            mo_file = po_file.replace('.po', '.mo')
            command = ['pybabel', 'compile', '-i', po_file, '-o', mo_file]
            subprocess.run(command, capture_output=True, text=True)
            print(f"Compiled {po_file} to {mo_file}")

def start_observer(path):
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")
        return
    event_handler = LocalizationHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    load_dotenv(re.sub(r'\\utils', '', os.path.abspath('configs\\.env')))
    pg = PathGetter()
    base_path = pg.check_env_var('APP_LOCALIZATION_WATCH_PATH')
    loc_versions = pg.get_param_list('APP_LANGUAGES')
    pages = pg.get_param_list('APP_PAGES')
    paths = [os.path.abspath(f'{base_path}/{page}/{version}/LC_MESSAGES/messages.po') for version, page in itertools.product(loc_versions, pages)]
    new_paths = [(re.sub(r'\\utils', '', path)) for path in paths]
    processes = []
    for path in new_paths:
        if os.path.exists(path):
            p = multiprocessing.Process(target=start_observer, args=(path,))
            p.start()
            processes.append(p)
        else:
            print(f"Path does not exist: {path}")
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in itertools.chain(processes, processes):
            p.terminate() if p.is_alive() else p.join()
