from opa.readers.baseReader import BaseLogFileReader
from opa.extractors import Substring


class NxLogFileReader(BaseLogFileReader):

    def __init__(self, directory: str, fileNamePattern: str):
        super(NxLogFileReader, self).__init__('Nx',
                                              directory,
                                              fileNamePattern,
                                              [
                                                  Substring('.logPerformance',
                                                            lambda line, i: {'Publish': int(line[i + 48:])},
                                                            category1='Performance'),
                                                  Substring('.handleConnect',
                                                            lambda line, i: {'IP': line[i + 17:]},
                                                            category1='Tcp', category2='Connect'),
                                                  Substring('.handleDisconnect',
                                                            lambda line, i: {'IP': line[i + 20:]},
                                                            category1='Tcp', category2='Disconnect')
                                              ])
