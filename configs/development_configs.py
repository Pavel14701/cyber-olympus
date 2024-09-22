import sass, os, re
from typing import Tuple
from abc import ABC
from flask_assets import Bundle, Environment
from configs.config_loader import EnvSingleton
from utils.path_getter import PathGetter


class AppSCSSCompiler(PathGetter, ABC):
    def __init__(self):
        PathGetter.__init__(self)
        ABC.__init__(self)
        EnvSingleton()

    def get_scss_compiler(self) -> None:
        scss_path = self.check_env_var('APP_SCSS_WATCH_PATH')
        save_base_path = re.sub(r'/scss', '', scss_path)
        pages = self.get_scss_filenames(scss_path)
        assets = Environment(self.app)
        for page in pages:
            css_file = self.__compile_scss(page, scss_path, save_base_path)
            css_bundle = Bundle(css_file, output=css_file)
            assets.register(f'{page}_css', css_bundle)
        print('ALL SCSS FILES COMPILED')

    def __compile_scss(self, page:str, scss_path:str, save_base_path:str) -> str:
        paths = self.__create_scss_save_paths(scss_path, page, save_base_path)
        compiled_css = sass.compile(
            filename=paths[0],
            output_style='expanded'
        )
        self.__save_output_style(paths[1], compiled_css)
        return paths[1]

    def __create_scss_save_paths(self, scss_path:str, page:str, save_base_path:str) -> Tuple[str]:
        scss_file = os.path.abspath(f'{scss_path}/{page}.scss')
        css_file = os.path.abspath(f'{save_base_path}/{page}/styles/{page}.css')
        map_file = os.path.abspath(f'{save_base_path}/{page}/styles/{page}.css.map')
        return (scss_file, css_file, map_file)

    def __save_output_style(self, filename:str, data:str) -> None:
        with open(filename, 'w') as css_out:
            css_out.write(data)

class AppDevelopmentConfigs(AppSCSSCompiler, ABC):
    def __init__(self):
        AppSCSSCompiler.__init__(self)
        EnvSingleton()