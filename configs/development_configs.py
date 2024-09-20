from abc import ABC
from flask_assets import Bundle, Environment
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppDevelopmentConfigs(PathGetter, ABC):
    def __init__(self):
        PathGetter.__init__(self)
        EnvSingleton()


    def get_scss_compiler(self) -> None:
        scss_path = self.check_env_var('APP_SCSS_WATCH_PATH')
        pages = self.get_scss_filenames(scss_path)
        assets = Environment(self.app)
        for page in pages:
            scss = Bundle(
                f'scss/{page}.scss',
                filters='libsass',
                output=f'{page}/styles/{page}.css'
            )
            assets.register(f'{page}_sccs', scss)
            scss.build()