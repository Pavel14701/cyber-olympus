from utils.path_getter import PathGetter
from flask_sqlalchemy import SQLAlchemy
from configs.config_loader import EnvSingleton
from abc import ABC

class AppSQLDatabaseConfigs(PathGetter, ABC):
    def __init__(self, db:SQLAlchemy) -> None:
        PathGetter.__init__(self)
        ABC.__init__(self)
        EnvSingleton()
        self.db = db


    def get_flask_db(self) -> SQLAlchemy:
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.check_env_var('SQLALCHEMY_DATABASE_URI')#'sqlite:///db.sqlite3'
        self.db.init_app(self.app)
        self.__create_tables()
        return self.db

    def __create_tables(self) -> None:
        with self.app.app_context():
            self.db.create_all()