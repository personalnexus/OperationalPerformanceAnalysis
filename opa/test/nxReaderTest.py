import unittest
from datetime import datetime
import opa.test


class NxTests(unittest.TestCase):

    def testLoadNxEntries(self):
        reader = opa.test.readNxLogFileEntries()
        self.assertIsNotNone(reader.logFileEntries)
        self.assertEqual(7, len(reader.logFileEntries))

        self.checkEntry(reader, 0, datetime(2019, 8, 15, 10, 0, 1), 'Performance', 12876)
        self.checkEntry(reader, 1, datetime(2019, 8, 15, 10, 0, 1), 'Tcp', 'Disconnect:10.2.4.27')
        self.checkEntry(reader, 2, datetime(2019, 8, 15, 10, 0, 42), 'Tcp', 'Connect:10.2.4.27')
        self.checkEntry(reader, 3, datetime(2019, 8, 15, 10, 1, 1), 'Performance', 9247)
        self.checkEntry(reader, 6, datetime(2019, 8, 19, 11, 2, 12), 'firstName', 'John')

    def checkEntry(self, reader, index, expectedTimestamp, key, expectedValue):
        self.assertEqual(expectedTimestamp, reader.logFileEntries[index].timestamp)
        self.assertEqual(expectedValue, reader.logFileEntries[index].data.get(key, None))
