from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    @staticmethod
    def get_env(env: str) -> str:
        return environ[env]
