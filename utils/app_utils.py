import os, inspect
from abc import ABC

class AppUtils:
    HTML = '.html'
    
    def page_name(self):
        name = inspect.currentframe().f_back.f_code.co_name
        self.load_translations(name)
        return name

    def __load_translations(self, page):
        translations_dir = os.path.join('translations', page)
        self.babel.translation_directories = translations_dir