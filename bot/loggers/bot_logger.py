import logging
from logging import Logger


class BotLogger(Logger):
    def __init__(self, name: str, level: int | str = 0) -> None:
        super().__init__(name, level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(levelname)s:\t"
            "%(filename)s."
            "%(funcName)s."
            "%(lineno)d:\t"
            "%(message)s",
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(logging.INFO)
