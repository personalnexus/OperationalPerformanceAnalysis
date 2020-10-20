from abc import ABC, abstractmethod
from typing import Callable, Any
from opa import columns
import re


class BaseExtractor(ABC):

    @abstractmethod
    def getDataFromLine(self, line: str) -> dict:
        pass


class Regex(BaseExtractor):

    def __init__(self, pattern, matchGroupIndex):
        self._pattern = re.compile(pattern)
        self._matchGroupIndex = matchGroupIndex

    def getDataFromLine(self, line: str) -> dict:
        match = self._pattern.search(line)
        result = match.group(self._matchGroupIndex) if match else None
        return result


class Substring(BaseExtractor):

    def __init__(self,
                 substring: str,
                 valueGetter: Callable[[str, int], dict],
                 category1: str = None,
                 category2: str = None):
        super(Substring, self).__init__()
        self._substring = substring
        self._category1 = category1
        self._category2 = category2
        self._valueGetter = valueGetter

    def getDataFromLine(self, line: str) -> dict:
        substringIndex = line.find(self._substring)
        if substringIndex >= 0:
            result = self._valueGetter(line, substringIndex)
            if result:
                if self._category1:
                    result[columns.Category1] = self._category1
                if self._category2:
                    result[columns.Category2] = self._category2
        else:
            result = None
        return result


class Func(BaseExtractor):

    def __init__(self, func: Callable[[str], dict]):
        self._func = func

    def getDataFromLine(self, line: str) -> dict:
        return self._func(line)