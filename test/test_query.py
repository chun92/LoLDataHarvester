import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util import config_loader

import unittest

from util.api_requester import LoLTier, LoLDivision
from util.api_requester import get_summoner_ids

config = config_loader.load_config()
key = config['api_keys'][0]

class TestGetSummonerIds(unittest.TestCase):
    def test_get_summoner_ids_with_diamond(self):
        for i in range(1, 200):
            ids = get_summoner_ids(key, tier=LoLTier.DIAMOND, division=LoLDivision.I, page=i)
            if ids is not None:
                print(f"Page {i}: success")
            else:
                print(f"Page {i}: failed")
            self.assertIsNotNone(ids)

if __name__ == '__main__':
    unittest.main()