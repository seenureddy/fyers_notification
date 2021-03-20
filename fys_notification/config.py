# Local imports

from fys_notification.utils import get_env

# third party imports
import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa: W1202
config_file_logger = logging.getLogger("config_file_log")


SMPT_SERVER = "smtp.gmail.com"
SMPT_PORT = "587"
FYS_SMPT_EMAIL = os.getenv("FYS_SMPT_EMAIL", "srinivasulur55.s@gmail.com")
FYS_SMPT_PASSWORD = os.getenv("FYS_SMPT_PASSWORD")
FYS_ADMIN_EMAIL = os.getenv("FYS_ADMIN_EMAIL", "srinivasulur55.s@gmail.com")


if get_env("LIFE_CYCLE") == "heroku":
    config_file_logger.info(get_env("LIFE_CYCLE"))
    SQLALCHEMY_DATABASE_URI = get_env("DATABASE_URL")
else:
    config_file_logger.info("local")
    POSTGRES_USER = "seenu"
    POSTGRES_URL = "localhost"
    POSTGRES_DB = "fyn_db"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}@{POSTGRES_URL}/{POSTGRES_DB}"

config_file_logger.debug(SQLALCHEMY_DATABASE_URI)
