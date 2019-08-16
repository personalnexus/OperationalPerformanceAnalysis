import os
from datetime import datetime


class LogFile(object):

    def __init__(self, directory, fileNamePattern, date):
        super(LogFile, self).__init__()
        self.date = datetime.date(date)
        fileName = date.strftime(fileNamePattern)
        self.fileName = os.path.join(directory, fileName)

    def getEntries(self, dataGetter):
        """
        :param dataGetter: Function to check whether the given line is relevant and if so, get data from it
        :return: List of all relevant log file entries
        :rtype: list[LogFileEntry]
        """
        result = []
        try:
            with open(self.fileName) as f:
                for line in f:
                    timestamp, data = dataGetter(line)
                    if data:
                        logFileEntry = LogFileEntry(line, self, timestamp, data)
                        result.append(logFileEntry)
        except IOError:
            pass
        return result


class LogFileEntry(object):

    def __init__(self, line, logFile, time, data):
        self.line = line
        self.logFile = logFile
        self.time = time
        self.data = data

    @property
    def timestamp(self):
        return datetime.combine(self.logFile.date, self.time)