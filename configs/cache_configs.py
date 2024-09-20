from abc import ABC
from flask_caching import Cache
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter 


class AppCacheConfigs(PathGetter, ABC):
    def __init__(self) -> None:
        super().__init__()
        EnvSingleton()

    def get_flask_cache(self) -> Cache:
        self.app.config['CACHE_TYPE'] = self.check_env_var('APP_CACHE_TYPE') #'RedisCache'
        self.app.config['CACHE_REDIS_HOST'] = self.check_env_var('APP_CACHE_REDIS_HOST') #'localhost'
        self.app.config['CACHE_REDIS_PORT'] = int(self.check_env_var('APP_CACHE_REDIS_PORT')) #6379
        self.app.config['CACHE_REDIS_DB'] = int(self.check_env_var('APP_CACHE_REDIS_DB')) #3
        self.app.config['CACHE_REDIS_URL'] = self.check_env_var('APP_CACHE_REDIS_URI') #'redis://localhost:6379/3'
        return Cache(self.app)