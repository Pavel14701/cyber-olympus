from abc import ABC
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_compress import Compress
from turbo_flask import Turbo
from datetime import timedelta
from configs.cache_configs import AppCacheConfigs
from configs.cdn_configs import AppCDNConfigs
from configs.config_loader import EnvSingleton
from configs.database_configs import AppSQLDatabaseConfigs
from configs.development_configs import AppDevelopmentConfigs
from configs.localization__configs import AppLocalizationConfigs
from configs.login_configs import AppLoginManagerConfigs
from configs.oauth_configs import AppOAuthConfigs
from configs.secret_configs import AppSecretConfigs
from configs.session_configs import AppSessionConfigs


class AppUtilsConfig(ABC):
    def __init__(self) -> None:
        super().__init__()
        EnvSingleton()
        
    def get_flask_turbo(self) -> Turbo:
        return Turbo(self.app)

    def get_flask_compress(self) -> Compress:
        self.app.config['COMPRESS_MIN_SIZE'] = 200
        self.app.config['COMPRESS_MIMETYPES'] = [
            'text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript',
            'text/plain', 'application/xml', 'application/xhtml+xml', 'application/rss+xml',
            'application/atom+xml', 'image/svg+xml', 'application/x-javascript',
            'application/x-font-ttf', 'application/vnd.ms-fontobject', 'font/opentype'
        ]
        self.cache.init_app(self.app)
        self.app.config['COMPRESS_CACHE_BACKEND'] = self.cache
        self.app.config['COMPRESS_CACHE_KEY'] = self.custom_cache_key
        return Compress(self.app)

    def custom_cache_key(self, response):
        return hash(response.data)

class AppConfigs(AppSecretConfigs, AppCacheConfigs, AppCDNConfigs, AppSessionConfigs,\
    AppSQLDatabaseConfigs, AppOAuthConfigs, AppLoginManagerConfigs, AppDevelopmentConfigs,\
        AppUtilsConfig, AppLocalizationConfigs, ABC):
    def __init__(self):
        EnvSingleton()
        self.app = Flask(self.check_env_var('APP_NAME'))
        self.app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
        self.app.config['SESSION_PROTECTION'] = self.check_env_var('strong')
        super().__init__()
        self.babel = self.get_flask_babel()

    def get_app(self) -> Flask: 
        self.create_localization_files()
        return self.app

    def get_port(self) -> int:
        return int(self.check_env_var('APP_PORT'))
    
    def get_oauth(self, oauth:str) -> OAuth:
        match oauth:
            case _ if oauth in self.oauth_services:
                return self.get_auth_client(oauth)
            case _:
                raise ValueError(f"Unknown config: {oauth}")
    
    def get_flask_babel(self):
        return self.babel