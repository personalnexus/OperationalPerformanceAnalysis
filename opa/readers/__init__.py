from os import path
from datetime import date, datetime, time
from typing import List
import numpy as np
import pandas as pd
import columns
from extractors import BaseExtractor
from extractors.canonical import CanonicalJson


class BaseLogFileReader(object):

    def __init__(self, applicationName: str, applicationInstance: str, extractors: List[BaseExtractor]):
        super(BaseLogFileReader, self).__init__()
        self._applicationName = applicationName
        self._applicationInstance = applicationInstance
        # TODO: make log directory a configuration parameter
        self._fileName = path.abspath('..\\..\\samples\\' +
                                      rf'{applicationName}\{applicationInstance}\{applicationName}_%Y_%m_%d_'
                                      rf'{applicationInstance}.log')
        self._extractors = extractors + [CanonicalJson()]

    def getEntriesAsDataFrame(self, relevantDates: List[date]) -> pd.DataFrame:
        entries = []
        for relevantDate in relevantDates:
            try:
                fileName = relevantDate.strftime(self._fileName)
                with open(fileName, mode='r') as f:
                    for line in f:
                        strippedLine = line.strip()
                        dataList = self.getDataListFromExtractors(strippedLine)
                        if dataList:
                            timePart = self.getTimestampFromLine(strippedLine)
                            timestamp = datetime.combine(relevantDate, timePart)
                            for data in dataList:
                                # add the pieces of information we already have here, so extractors don't have to
                                data[columns.Application] = self._applicationName
                                data[columns.Instance] = self._applicationInstance
                                data[columns.Timestamp] = timestamp
                                data[columns.FileName] = fileName
                                entries.append(data)
            except IOError:
                pass

        return self.getDataFrameFromDataList(entries)

    def getDataListFromExtractors(self, line) -> List[dict]:
        """
        Override in derived classes to add specific processing of the given line
        """
        result = []
        for extractor in self._extractors:
            extractedData = extractor.getDataFromLine(line)
            # Extractors may return either nothing, a single dictionary or an iterable
            if extractedData is not None:
                if isinstance(extractedData, dict):
                    result.append(extractedData)
                else:
                    result.extend(extractedData)
        return result

    # noinspection PyMethodMayBeStatic
    def getDataFrameFromDataList(self, entries: List[dict]) -> pd.DataFrame:
        """
        Creates a DataFrame with each of the given dictionaries as a row. Override for additional processing of the
        data in the DataFrame
        """
        index = np.arange(0, len(entries))
        result = pd.DataFrame(data=entries, index=index)
        return result

    # noinspection PyMethodMayBeStatic
    def getTimestampFromLine(self, line) -> time:
        """
        Extracts the time (not the date!) from the given line. Override in derived classes for different date format
        """
        result = datetime.time(datetime.strptime(line[:8], '%H:%M:%S'))
        return result
