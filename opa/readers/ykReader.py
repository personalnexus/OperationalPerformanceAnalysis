from opa import BaseLogFileReader
from opa.extractors.keyValue import CategoryKeyValueSubstring


class YkLogFileReader(BaseLogFileReader):

    def __init__(self, applicationInstance: str):
        super(YkLogFileReader, self).__init__('Yk',
                                              applicationInstance,
                                              [
                                                  CategoryKeyValueSubstring('.dumpPerformanceStatistics',
                                                                            category1='Performance',
                                                                            defaultCategory2='General')
                                              ])
