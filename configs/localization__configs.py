import os, subprocess
from abc import ABC
from flask_babel import Babel
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppLocalizationConfigs(PathGetter, ABC):
    def __init__(self):
        PathGetter.__init__(self)
        EnvSingleton()

    def get_flask_babel(self) -> Babel:
        self.app.config['LANGUAGES'] = self.get_param_list('APP_LANGUAGES')
        self.app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
        self.app.config['BABEL_DEFAULT_LOCALE'] = 'en'
        self.app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
        return Babel(self.app)

    def create_localization_files(self):
        base_dir = 'translations/'
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.po'):
                    po_file = os.path.join(root, file)
                    mo_file = po_file.replace('.po', '.mo')
                    subprocess.run(['pybabel', 'compile', '-i', po_file, '-o', mo_file])