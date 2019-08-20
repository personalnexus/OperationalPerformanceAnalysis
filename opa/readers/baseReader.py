import os
from datetime import datetime
from opa.logFiles import LogFile, LogFileEntry, TimestampColumn
import json
import numpy as np
import pandas as pd


class BaseLogFileReader(object):

    def __init__(self, directory, fileNamePattern, relevantDates):
        super(BaseLogFileReader, self).__init__()
        absoluteDirectory = os.path.abspath(directory)
        self._logFiles = [LogFile(absoluteDirectory, fileNamePattern, date) for date in relevantDates]
        self.logFileEntries = []  # type: list[LogFileEntry]

    def loadLogFileEntries(self):
        self.logFileEntries = []
        for logFile in self._logFiles:
            self.logFileEntries.extend(logFile.getEntries(self.getDataFromLine))

    def getDataFromLine(self, line):
        """
        Check if canonical logging is found, otherwise delegate to derived class
        """
        substringIndex = line.find('.logCanonicalJson')
        if substringIndex < 0:
            result = self.getDataFromLineCore(line)
        else:
            time = self.getTimeFromLine(line)
            data = json.loads(line[substringIndex+17:])
            result = time, data
        return result

    # noinspection PyUnusedLocal
    def getDataFromLineCore(self, line):
        """
        Override in derived classes to indicate whether to use the given line
        :param line:
        :return: True if the line is to be used, otherwise False
        :rtype: dict
        """
        return None

    def getDataFromSubstringInLine(self, line, parameters):
        """
        Can be called from derived classes to extract text when a given substring is found
        :param line: the line to search
        :param parameters: tuple of substring, key and valueGetter
        :return: tuple of time and the extracted value from the first substring that was found
        """
        for (substring, key, valueGetter) in parameters:
            substringIndex = line.find(substring)
            if substringIndex >= 0:
                time = self.getTimeFromLine(line)
                value = valueGetter(substringIndex)
                data = {key: value}
                result = time, data
                break
        else:
            result = (None, None)
        return result

    # noinspection PyMethodMayBeStatic
    def getTimeFromLine(self, line):
        """
        Extracts the time (not the date!) from the given line. Override in derived classes for different date format
        :param line: the current line
        :return:
        :rtype: datetime
        """
        result = datetime.time(datetime.strptime(line[:8], '%H:%M:%S'))
        return result

    def toDataFrame(self):
        data = [entry.getFullData() for entry in self.logFileEntries]
        index = np.arange(0, len(data))
        result = pd.DataFrame(data, index)
        result.set_index(TimestampColumn, inplace=True)
        return result
