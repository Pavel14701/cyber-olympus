import itertools
import multiprocessing
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler , FileModifiedEvent
import time
import os, re
from path_getter import PathGetter



class TSHandler(FileSystemEventHandler):
    def on_modified(self, event: FileModifiedEvent):
        if event.src_path.endswith('.ts'):
            print(f"Detected change in {event.src_path}. Compiling TypeScript to JavaScript using Node.js...")
            filename = os.path.basename(event.src_path).replace('.ts', '')
            print(filename)
            output_dir = re.sub(r'\\utils', '', os.path.abspath(f'static/{filename}/js/'))
            print(output_dir)
            output_file = os.path.join(output_dir, f'{filename}.js')
            os.makedirs(output_dir, exist_ok=True)
            command = ['npx', 'tsc', '--outDir', output_dir, event.src_path]
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                print(f"Ошибка выполнения команды\n\
                    Код возврата: {result.returncode}\n\
                        Стандартный вывод: {result.stdout}\n\
                            Стандартный вывод ошибок: {result.stderr}")
            print(f"Compiled {event.src_path} to {output_file}")


class SCSSHandler(FileSystemEventHandler):
    def on_modified(self, event:FileModifiedEvent):
        if event.src_path.endswith('.scss'):
            print(f"Detected change in {event.src_path}. Compiling SCSS to CSS using python sass...")
            filename = os.path.basename(event.src_path).replace('.scss', '')
            print(filename)
            output_dir = re.sub(r'\\utils', '', os.path.abspath(f'static/{filename}/styles/'))
            print(output_dir)
            output_file = os.path.join(output_dir, f'{filename}.css')
            os.makedirs(output_dir, exist_ok=True)
            result = subprocess.run(['sass', event.src_path, output_file], shell=True, capture_output=True)
            if result.returncode != 0:
                print(f"Ошибка выполнения команды\n\
                    Код возврата: {result.returncode}\n\
                        Стандартный вывод: {result.stdout}\n\
                            Стандартный вывод ошибок: {result.stderr}")
            print(f"Compiled {event.src_path} to {output_file}")


class Watcher(PathGetter):
    def __init__(self, type_file:str):
        self.type_file = type_file

        
    def __create_observer(self):
        observer = Observer()
        if self.type_file == '.scss':
            path = re.sub(r'\\utils', '', os.path.abspath("static/scss"))
            observer.schedule(SCSSHandler(), path, recursive=True)
        else:
            path = re.sub(r'\\utils', '', os.path.abspath("static/ts"))
            observer.schedule(TSHandler(), path, recursive=True)
        observer.start()
        print(f"Watching for changes in {path}...")
        return observer

    def start_watching(self):
        observer = self.__create_observer()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def run():
    types = ['.scss', '.ts']
    processes = [multiprocessing.Process(target=Watcher(_type).start_watching) for _type in types]
    try:
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    except KeyboardInterrupt:   
        for p in itertools.chain(processes, processes):
            p.terminate() if p.is_alive() else p.join()

if __name__ == '__main__':
    run()