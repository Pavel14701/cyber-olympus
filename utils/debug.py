import multiprocessing, subprocess, os

def run_script(script_name):
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        print(line.decode().strip())
    for line in process.stderr:
        print(line.decode().strip())

def start_app():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    app = os.path.join(parent_dir, 'main.py')
    scss_handler = os.path.join(os.path.dirname(__file__), 'watch_scss.py')
    p1 = multiprocessing.Process(target=run_script, args=(app,))
    p2 = multiprocessing.Process(target=run_script, args=(scss_handler,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    start_app()