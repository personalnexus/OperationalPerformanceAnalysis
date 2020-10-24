from typing import Callable
from extractors import BaseExtractor


class Func(BaseExtractor):

    def __init__(self, func: Callable[[str], dict]):
        self._func = func

    def getDataFromLine(self, line: str) -> dict:
        return self._func(line)