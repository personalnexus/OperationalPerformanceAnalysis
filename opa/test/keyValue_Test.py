import unittest
from typing import List
from opa import columns
from opa.extractors.keyValue import CategoryKeyValueSubstring


class KeyValueTests(unittest.TestCase):

    def testKeyValueWithoutCategories(self):
        dicts = self._runExtractor('key1=value1;key2=value2')
        self.assertEqual(1, len(dicts))
        self.assertEqual({columns.Category1: 'Perf',
                          columns.Category2: 'Misc',
                          'key1': 'value1',
                          'key2': 'value2'},
                         dicts[0])

    def testKeyValueWithTwoCategories(self):
        dicts = self._runExtractor('A.key1=value1a;B.key1=value1b')
        self.assertEqual(2, len(dicts))
        self.assertEqual({columns.Category1: 'Perf',
                          columns.Category2: 'A',
                          'key1': 'value1a'},
                         dicts[0])
        self.assertEqual({columns.Category1: 'Perf',
                          columns.Category2: 'B',
                          'key1': 'value1b'},
                         dicts[1])

    def _runExtractor(self, keyValueString: str) -> List[dict]:
        extractor = CategoryKeyValueSubstring('DumpPerf', category1='Perf', defaultCategory2='Misc')
        result = extractor.getDataFromLine(f'20:25:37 INFO DumpPerf {keyValueString}')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        return result
