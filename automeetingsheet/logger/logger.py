import logging
import traceback

LOG_FILE_PATH = "logs/error.log"


class Logger:
    def __init__(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(LOG_FILE_PATH)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    # エラーが起きた際に呼び出すことで、エラーの詳細をログに残す
    def error(self):
        self.logger.error(traceback.format_exc())
