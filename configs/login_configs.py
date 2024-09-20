from abc import ABC
from flask_login import LoginManager
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter
from flask_babel import _


class AppLoginManagerConfigs(PathGetter, ABC):
    def __init__(self):
        PathGetter.__init__(self)
        EnvSingleton()
        self.login_url = self.check_env_var('LOGIN_URL')

    def get_flask_login_manager(self) -> LoginManager:
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = self.login_url
        self.login_manager.login_message = _("Please log in to access this page.")
        self.login_manager.login_message_category = "info"
        self.login_manager.refresh_view = 'relogin'
        self.login_manager.needs_refresh_message = _("To protect your account, please reauthenticate to access this page.")
        self.login_manager.needs_refresh_message_category = "info"
        return self.login_manager