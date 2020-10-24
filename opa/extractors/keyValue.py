from typing import List
from extractors import BaseExtractor
from opa import columns


class CategoryKeyValueSubstring(BaseExtractor):

    def __init__(self,
                 substring: str,
                 category1: str,
                 defaultCategory2: str,
                 keyValueSeparator: str = '=',
                 keyValuePairsSeparator: str = ';',
                 categoryKeySeparator: str = '.'):
        self._substring = substring
        self._category1 = category1
        self._defaultCategory2 = defaultCategory2
        self._keyValueSeparator = keyValueSeparator
        self._keyValuePairsSeparator = keyValuePairsSeparator
        self._categoryKeySeparator = categoryKeySeparator

    def getDataFromLine(self, line: str) -> List[dict]:
        resultDictByCategory2 = {}
        substringIndex = line.find(self._substring)
        if substringIndex >= 0:
            keyValuePairs = line[substringIndex + len(self._substring) + 1:]
            for keyValuePair in keyValuePairs.split(self._keyValuePairsSeparator):
                categoryAndKey, value = keyValuePair.split(self._keyValueSeparator, maxsplit=1)
                categoryKeySeparatorIndex = categoryAndKey.find(self._categoryKeySeparator)

                if categoryKeySeparatorIndex >= 0:
                    category2 = categoryAndKey[:categoryKeySeparatorIndex]
                    key = categoryAndKey[categoryKeySeparatorIndex+1:]
                else:
                    category2 = self._defaultCategory2
                    key = categoryAndKey

                if category2 in resultDictByCategory2:
                    resultDict = resultDictByCategory2[category2]
                else:
                    # initialize each line with its categories
                    resultDict = {
                        columns.Category1: self._category1,
                        columns.Category2: category2
                    }
                    resultDictByCategory2[category2] = resultDict
                resultDict[key] = value

        return list(resultDictByCategory2.values())
