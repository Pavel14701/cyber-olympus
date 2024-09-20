from abc import ABC
from typing import Optional
from flask_cdn import CDN
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppCDNConfigs(PathGetter, ABC):
    def __init__(self) -> None:
        PathGetter.__init__(self)
        EnvSingleton()
        self.__get_cdn_configs()

    def __get_cdn_configs(self) -> None:
        self.use_cdn = bool(self.check_env_var('APP_USE_CDN'))
        if self.use_cdn:
            self.app.config['CDN_DOMAIN'] = self.check_env_var('APP_CDN_DOMAIN')

    def get_flask_cdn(self) -> Optional[CDN]:
        if self.use_cdn:
            return CDN(self.app)
        print('CDN is not used')
        return None