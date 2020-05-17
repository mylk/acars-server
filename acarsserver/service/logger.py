import logging
from logging import handlers
from sys import stdout

from acarsserver.config import environment


class LoggerService:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(environment.logging_level)

        rotate_handler = handlers.TimedRotatingFileHandler(
            filename=environment.logging_file,
            when="midnight"
        )
        rotate_handler.suffix = "%Y%m%d"
        rotate_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(rotate_handler)

        stdout_handler = logging.StreamHandler(stdout)
        stdout_handler.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s - %(message)s"))
        self.logger.addHandler(stdout_handler)

    def get_instance(self):
        return self.logger
