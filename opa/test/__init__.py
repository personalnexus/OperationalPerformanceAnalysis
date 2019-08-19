from datetime import datetime
from opa.readers.nxReader import NxLogFileReader


def readNxLogFileEntries():
    reader = NxLogFileReader('..\\..\\samples\\Nx', 'Nx_%Y_%m_%d_PROD.log',
                             [datetime(2019, 8, 15), datetime(2019, 8, 19)])
    reader.loadLogFileEntries()
    return reader
