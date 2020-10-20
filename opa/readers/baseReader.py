import os
from typing import List
from datetime import date, time, datetime
from opa import columns
from opa.extractors import BaseExtractor
import json
import numpy as np
import pandas as pd


class BaseLogFileReader(object):

    def __init__(self, source: str, directory: str, fileNamePattern: str, extractors: List[BaseExtractor]):
        super(BaseLogFileReader, self).__init__()
        self._source = source
        self._directory = os.path.abspath(directory)
        self._fileNamePattern = fileNamePattern
        self._extractors = extractors

    def getEntriesAsDataFrame(self, relevantDates: List[date]) -> pd.DataFrame:
        entries = []
        for relevantDate in relevantDates:
            try:
                fileName = os.path.join(self._directory, relevantDate.strftime(self._fileNamePattern))
                with open(fileName, mode='r') as f:
                    for line in f:
                        strippedLine = line.strip()
                        dataList = self.getDataListFromLine(strippedLine)
                        if dataList:
                            timePart = self.getTimestampFromLine(strippedLine)
                            timestamp = datetime.combine(relevantDate, timePart)
                            for data in dataList:
                                # add the pieces of information we already have here, so extractors don't have to
                                data[columns.Source] = self._source
                                data[columns.Timestamp] = timestamp
                                data[columns.FileName] = fileName
                                entries.append(data)
            except IOError:
                pass

        index = np.arange(0, len(entries))
        result = pd.DataFrame(data=entries, index=index)
        return result

    def getDataListFromLine(self, line):
        """
        Check if canonical logging is found, otherwise delegate to derived class and/or extractors
        """
        canonicalSubstringIndex = line.find('.logCanonicalJson')
        if canonicalSubstringIndex < 0:
            result = self.getDataListFromExtractors(line)
        else:
            result = [json.loads(line[canonicalSubstringIndex + 17:])]
        return result

    # noinspection PyUnusedLocal
    def getDataListFromExtractors(self, line) -> List[dict]:
        """
        Override in derived classes to add specific processing of the given line
        :param line:
        :return: True if the line is to be used, otherwise False
        :rtype: dict
        """
        result = [data for data in (extractor.getDataFromLine(line) for extractor in self._extractors) if data]
        return result

    # noinspection PyMethodMayBeStatic
    def getTimestampFromLine(self, line) -> time:
        """
        Extracts the time (not the date!) from the given line. Override in derived classes for different date format
        :param line: the current line
        :return:
        :rtype: datetime
        """
        result = datetime.time(datetime.strptime(line[:8], '%H:%M:%S'))
        return result
