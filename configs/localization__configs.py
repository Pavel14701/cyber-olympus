import os, subprocess
from abc import ABC
from flask import request
from flask_babel import Babel
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppLocalizationConfigs(PathGetter, ABC):
    def __init__(self, compile_loc:bool=False):
        self.compike_loc = compile_loc
        PathGetter.__init__(self)
        ABC.__init__(self)
        EnvSingleton()

    def get_flask_babel(self) -> Babel:
        self.app.config['LANGUAGES'] = self.get_param_list('APP_LANGUAGES')
        self.app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
        self.app.config['BABEL_DEFAULT_LOCALE'] = 'en'
        self.app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
        babel = Babel(self.app, locale_selector=self.get_locale)
        babel.init_app(self.app)
        return babel

    def create_localization_files(self):
        if self.compike_loc:
            for root, dirs, files in os.walk('translations/'):
                for file in files:
                    if file.endswith('.po'):
                        po_file = os.path.join(root, file)
                        mo_file = po_file.replace('.po', '.mo')
                        subprocess.run(['pybabel', 'compile', '-i', po_file, '-o', mo_file])

    def get_locale(self):
        return request.accept_languages.best_match(['en', 'ru', 'es'])