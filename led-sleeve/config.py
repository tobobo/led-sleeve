import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.auth_site_base = os.getenv('AUTH_SITE_BASE')
        self.device_name = os.getenv('DEVICE_NAME')


config = Config()
