from abc import ABC, abstractmethod


class BaseExtractor(ABC):

    @abstractmethod
    def getDataFromLine(self, line: str) -> dict:
        pass


