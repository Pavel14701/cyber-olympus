from abc import ABC
from authlib.integrations.flask_client import OAuth
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppOAuthConfigs(PathGetter, ABC):
    def __init__(self) -> None:
        PathGetter.__init__(self)
        ABC.__init__(self)
        EnvSingleton()
        self.__get_oauth_configs()

    def __get_oauth_configs(self) -> None:
        self.oauth = OAuth(self.app)
        self.oauth_services = self.get_param_list(key='APP_OAUTH_LIST')
        self.oauth_clients = self.__create_oauth_configs()

    def __create_oauth_configs(self) -> dict:
        # USE APPER FOR FIRST WORD IN ENV KEY
        oauth_configs = {}
        for name in self.oauth_services:
            config = {
                'client_id': self.check_custom_env_var(name, 'access_token'), #auto uppercased
                'client_secret': self.check_custom_env_var(name, 'access_token_secret'),
                'request_token_url': self.check_custom_env_var(name, 'request_token_url'),
                'authorize_url': self.check_custom_env_var(name, 'authorize_url'),
                'access_token_url': self.check_custom_env_var(name, 'access_token_url'),
                'client_kwargs': {
                    'redirect_uri': self.check_custom_env_var(name, 'oauth_url_callback')
                    }
            }
            oauth_configs[name] = config
        return oauth_configs

    def __get_auth_clients(self) -> dict:
        return {
            name: self.oauth.register(
                name,
                client_id=config['client_id'],
                client_secret=config['client_secret'],
                request_token_url=config['request_token_url'],
                authorize_url=config['authorize_url'],
                access_token_url=config['access_token_url'],
                client_kwargs=config['client_kwargs']
            )
            for name, config in self.__create_oauth_configs().items()
        }

    def get_auth_client(self, name) -> OAuth:
        if not self.oauth_clients:
            self.oauth_clients= self.__get_auth_clients()
        return self.oauth_clients.get(name)