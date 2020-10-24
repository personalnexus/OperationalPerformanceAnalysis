import unittest
from datetime import datetime
from opa.readers.nxReader import NxLogFileReader


class NxTests(unittest.TestCase):

    def testLoadNxEntries(self):
        reader = NxLogFileReader('PROD')
        df = reader.getEntriesAsDataFrame([datetime(2019, 8, 15), datetime(2019, 8, 19)])
        self.assertEqual((7, 11), df.shape)
        self.assertEqual(['Application', 'Category1', 'Category2', 'FileName', 'IP', 'Instance', 'Publish', 'Timestamp',
                          'firstName', 'isAlive', 'lastName'],
                         list(df.columns))
        print()
        print(df.info())
        print(df)
