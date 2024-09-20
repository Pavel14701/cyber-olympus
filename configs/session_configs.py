from abc import ABC
from redis import Redis
from flask_session import Session
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppSessionConfigs(PathGetter, ABC):
    def __init__(self):
        PathGetter.__init__(self)
        EnvSingleton()

    def get_flask_session(self) -> Session:
        #filesystem или 'redis', 'memcached' и др.
        self.app.config['SESSION_TYPE'] = self.check_env_var('APP_SESSION_TYPE')
        self.app.config['SESSION_REDIS'] = Redis(
            host=self.check_env_var('APP_SESSION_REDIS_HOST'),
            port=self.check_env_var('APP_SESSION_REDIS_PORT'),
            db=self.check_env_var('APP_SESSION_REDIS_DB'))
        return Session(self.app)