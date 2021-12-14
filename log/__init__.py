import logging.config
from logging import Logger

import yaml

from config import APP_NAME


def logger() -> Logger:
    return logging.getLogger(name=APP_NAME)


def get_log_config() -> dict:
    with open("log/log-config.yaml", 'r') as cf:
        config = yaml.safe_load(cf.read())
    return config
