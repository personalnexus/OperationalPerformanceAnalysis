import json
from typing import Optional
from extractors import BaseExtractor


class CanonicalJson(BaseExtractor):

    def getDataFromLine(self, line: str) -> Optional[dict]:
        canonicalSubstringIndex = line.find('.logCanonicalJson')
        result = json.loads(line[canonicalSubstringIndex + 17:]) if canonicalSubstringIndex >= 0 else None
        return result
