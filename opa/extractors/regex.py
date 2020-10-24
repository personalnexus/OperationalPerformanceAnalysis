import re
from extractors import BaseExtractor


class Regex(BaseExtractor):

    def __init__(self, pattern, matchGroupIndex):
        self._pattern = re.compile(pattern)
        self._matchGroupIndex = matchGroupIndex

    def getDataFromLine(self, line: str) -> dict:
        match = self._pattern.search(line)
        result = match.group(self._matchGroupIndex) if match else None
        return result
