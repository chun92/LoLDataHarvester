import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util import config_loader
from util.api_requester import LoLRegion, LoLApi, LoLQueue, LoLTier, LoLDivision
from util.api_requester import get_summoner_ids, get_puuid, get_match_ids, get_match

import unittest

config = config_loader.load_config()
key = config['api_keys'][0]

class TestErrorCase(unittest.TestCase):
    def test_parse1(self):
        result = get_match(key, "KR_6929786175")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()