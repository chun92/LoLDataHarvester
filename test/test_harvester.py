import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util import config_loader
from util.api_requester import LoLTier
from util.db_manager import init_db
from app import harvester

import unittest

config = config_loader.load_config()
key = config['api_keys'][0]

class TestHarvester(unittest.TestCase):
    def test_get_summoners_challenger(self):
        summoners = harvester.get_summoners(key, LoLTier.CHALLENGER)
        self.assertIsNotNone(summoners)
        self.assertGreater(len(summoners), 0)

    def test_get_summoners_master(self):
        summoners = harvester.get_summoners(key, LoLTier.MASTER)
        self.assertIsNotNone(summoners)
        self.assertGreater(len(summoners), 0)

    def test_get_summoners_diamond(self):
        summoners = harvester.get_summoners(key, LoLTier.DIAMOND)
        self.assertIsNotNone(summoners)
        self.assertGreater(len(summoners), 0)

    def test_harvest(self):
        init_db(path='../db/test.db')
        harvester.harvest(key, LoLTier.CHALLENGER, maximum=5)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()