import pickle
from cryptography.fernet import Fernet
import threading
from redis import Redis


class TwitterTasks:
    def __init__(self):
        self.filename = 'twitter_social_tasks.pickle'
        self.keyfile = 'key.key'
        self.cipher_suite = self.__load_or_generate_key()
        self.lock = threading.Lock()
        self.__initialize_file()


    def __load_or_generate_key(self) -> Fernet:
        try:
            with open(self.keyfile, 'rb') as key_file:
                key = key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.keyfile, 'wb') as key_file:
                key_file.write(key)
        return Fernet(key)


    def __initialize_file(self):
        try:
            with open(self.filename, 'rb') as file:
                pickle.load(file)
        except (FileNotFoundError, EOFError):
            with open(self.filename, 'wb') as file:
                encrypted_data = self.cipher_suite.encrypt(pickle.dumps([]))
                pickle.dump(encrypted_data, file)


    def get(self):
        with self.lock:
            try:
                with open(self.filename, 'rb') as file:
                    encrypted_data = pickle.load(file)
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                return pickle.loads(decrypted_data)
            except Exception as e:
                return []


    def set(self, *args: str):
        with self.lock:
            current_data = self.get()
            current_data.extend(args)
            encrypted_data = self.cipher_suite.encrypt(pickle.dumps(current_data))
            with open(self.filename, 'wb') as file:
                pickle.dump(encrypted_data, file)


    def delete(self, *args: str):
        with self.lock:
            current_data = self.get()
            for arg in args:
                if arg in current_data:
                    current_data.remove(arg)
            encrypted_data = self.cipher_suite.encrypt(pickle.dumps(current_data))
            with open(self.filename, 'wb') as file:
                pickle.dump(encrypted_data, file)
