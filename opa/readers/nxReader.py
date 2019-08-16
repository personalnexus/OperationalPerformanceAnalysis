from baseReader import BaseLogFileReader
from datetime import datetime


class NxLogFileReader(BaseLogFileReader):

    def __init__(self, directory, fileNamePattern, relevantDates):
        super(NxLogFileReader, self).__init__(directory, fileNamePattern, relevantDates)

    def getDataFromLine(self,
                        line  # type: str
                        ):
        i = line.find('.logPerformance')
        if i < 0:
            result = (None, None)
        else:
            time = datetime.time(datetime.strptime(line[:8], '%H:%M:%S'))
            performance = line[i+48:]  # 48 is the length of the filler text
            data = {'Performance': int(performance)}
            result = time, data
        return result
