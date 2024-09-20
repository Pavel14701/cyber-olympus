from dotenv import load_dotenv


class EnvSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvSingleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        if self._initialized:
            return
        load_dotenv()
        self._initialized = True