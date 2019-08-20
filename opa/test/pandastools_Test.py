import unittest
import numpy as np
import pandas as pd
import opa.tools.pandas as pdt


class PandasTest(unittest.TestCase):

    dfExpected = pd.DataFrame({'A': [1.0, 2.0, 3.0],
                               'B': [1.0, 2.0, 3.0],
                               'C': [2.0, 2.0, 2.0]
                               })
    dfInput = pd.DataFrame({'A': [1.0, 2.0, 3.0],
                            'B': [1.0, np.nan, 3.0],
                            'C': [2.0, np.nan, np.nan]
                            })

    def testFillNa(self):
        pdt.fillNa(self.dfInput, lambda col: col.mean())
        print("\nActual:\n" + str(self.dfInput))
        print("\nExpected:\n" + str(self.dfExpected))
        self.assertTrue(self.dfExpected.equals(self.dfInput))
