import binascii, os
from dotenv import set_key
from abc import ABC
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter

class AppSecretConfigs(PathGetter, ABC):
    def __init__(self) -> None:
        super().__init__()
        EnvSingleton()

    def __check_secret_key(self) -> bytes:
        config_value = os.getenv('SECRET_KEY')
        if not config_value:
            set_key(dotenv_path='.env', key_to_set='SECRET_KEY', value_to_set=self.__create_secret_key())
        return self.__get_secret_key()

    def __create_secret_key(self) -> str:
        return binascii.hexlify(os.urandom(32)).decode()

    def __get_secret_key(self) -> bytes:
        return binascii.unhexlify(os.getenv('SECRET_KEY'))

    def get_secret_configs(self) -> None:
        self.app.secret_key = self.__check_secret_key()
        self.app.config['SECRET_KEY'] = self.__check_secret_key()
        self.app.config['COMPRESS_ALGORITHM'] = self.check_env_var('APP_COMPRESS_ALGORITHM')#'brotli'