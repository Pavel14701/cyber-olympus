from abc import ABC
from flask_caching import Cache
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter 


class AppCacheConfigs(PathGetter, ABC):
    def __init__(self) -> None:
        PathGetter.__init__(self)
        ABC.__init__(self)
        EnvSingleton()


    def get_flask_cache(self) -> Cache:
        self.app.config['CACHE_TYPE'] = self.check_env_var('APP_CACHE_TYPE') #'RedisCache'
        self.app.config['CACHE_REDIS_HOST'] = self.check_env_var('APP_CACHE_REDIS_HOST') #'localhost'
        self.app.config['CACHE_REDIS_PORT'] = int(self.check_env_var('APP_CACHE_REDIS_PORT')) #6379
        self.app.config['CACHE_REDIS_DB'] = int(self.check_env_var('APP_CACHE_REDIS_DB')) #3
        self.app.config['CACHE_REDIS_URL'] = self.check_env_var('APP_CACHE_REDIS_URI') #'redis://localhost:6379/3'
        cache = Cache(self.app)
        cache.init_app(self.app)
        return cache