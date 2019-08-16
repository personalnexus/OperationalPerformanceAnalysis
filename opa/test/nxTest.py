import unittest
from datetime import datetime
from opa.readers.nxReader import NxLogFileReader


class NxTests(unittest.TestCase):

    def testLoadNxEntries(self):
        reader = NxLogFileReader('..\\..\\samples\\Nx', 'Nx_%Y_%m_%d_PROD.log', [datetime(2019, 8, 15)])
        reader.loadLogFileEntries()
        self.assertIsNotNone(reader.logFileEntries)
        self.assertEqual(2, len(reader.logFileEntries))

        self.assertEqual(datetime(2019, 8, 15, 10, 0, 1), reader.logFileEntries[0].timestamp)
        self.assertEqual(12876, reader.logFileEntries[0].data.get("Performance", None))

        self.assertEqual(datetime(2019, 8, 15, 10, 1, 1), reader.logFileEntries[1].timestamp)
        self.assertEqual(9247, reader.logFileEntries[1].data.get("Performance", None))
