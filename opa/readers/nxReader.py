from baseReader import BaseLogFileReader


class NxLogFileReader(BaseLogFileReader):

    def __init__(self, directory, fileNamePattern, relevantDates):
        super(NxLogFileReader, self).__init__(directory, fileNamePattern, relevantDates)

    def getDataFromLineCore(self, line):
        result = self.getDataFromSubstringInLine(line,
                                                 [('.logPerformance', 'Performance', lambda i: int(line[i + 48:])),
                                                  ('.handleConnect', 'Tcp', lambda i: 'Connect:' + line[i + 17:]),
                                                  ('.handleDisconnect', 'Tcp', lambda i: 'Disconnect:' + line[i + 20:])]
                                                 )
        return result
