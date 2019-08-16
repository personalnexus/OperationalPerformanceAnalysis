import abc
import os
from opa.logFiles import LogFile, LogFileEntry


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

    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def getDataFromLine(self, line):
        """
        Override in derived classes to indicate whether to use the given line
        :param line:
        :return: True if the line is to be used, otherwise False
        :rtype: dict
        """
        return None
