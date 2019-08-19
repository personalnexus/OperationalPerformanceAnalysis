import unittest
import opa.test


class LogFilesTest(unittest.TestCase):

    def testEntriesToDataFrame(self):
        reader = opa.test.readNxLogFileEntries()
        df = reader.toDataFrame()
        self.assertEquals((7, 5), df.shape)
        print df
