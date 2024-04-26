import logging
from logging import Logger
from typing import Union


class DetaLogger(Logger):
    def __init__(self, name: str, level: Union[int, str] = 0) -> None:
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
