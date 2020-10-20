import unittest
from datetime import datetime
from opa.readers.nxReader import NxLogFileReader


class NxTests(unittest.TestCase):

    def testLoadNxEntries(self):
        reader = NxLogFileReader('..\\..\\samples\\Nx', 'Nx_%Y_%m_%d_PROD.log')
        df = reader.getEntriesAsDataFrame([datetime(2019, 8, 15), datetime(2019, 8, 19)])
        self.assertEqual((7, 10), df.shape)
        print()
        print(df)
