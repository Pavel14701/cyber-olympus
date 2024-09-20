import os
from abc import ABC

class PathGetter(ABC):
    def get_param_list(self, key:str) -> tuple:
        if services_str := os.getenv(f'{key.upper()}'):
            return tuple(services_str.split(',')) if ',' in services_str else (services_str,)
        else:
            raise ValueError(f'Missing parameters for {key.upper()}')
    
    def check_env_var(self, var_name:str) -> str:
        value = os.getenv(var_name.upper())
        if value is None:
            raise ValueError(f"Environment variable '{var_name.upper()}' is not set")
        return value

    def get_scss_filenames(self, directory:str) -> tuple:
        files = [os.path.splitext(file)[0] for file in os.listdir(directory) if file.endswith('.scss')]
        return tuple(files)

    def check_custom_env_var(self, name:str, var_name:str) -> str:
        var = f'{name.upper()}_{var_name.upper()}'
        value = os.getenv(var)
        if value is None:
            raise ValueError(f"Environment variable '{var_name.upper()}' is not set")
        return value