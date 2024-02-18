import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

import unittest

from util.api_requester import LoLTier
from util.csv_manager import append_to_csv, read_and_print_champion_names_from_csv

class TestCsvManager(unittest.TestCase):
    def test_append_to_csv(self):
        obj = {
            "game_version": "14.3.558.8314",
            "game_duration": 1729,
            100: {
                'TOP': 80,
                'JUNGLE': 120,
                'MIDDLE': 103,
                'BOTTOM': 360,
                'UTILITY': 57,
                'win': True,
                'bans': [4, 901, 236, 24, 104]
            },
            200: {
                'TOP': 79,
                'JUNGLE': 200,
                'MIDDLE': 157,
                'BOTTOM': 101,
                'UTILITY': 235,
                'win': False,
                'bans': [53, 555, 86, 268, 4]
            }
        }
        tier = LoLTier.CHALLENGER
        append_to_csv(obj, tier, csv_path='../results/test.csv')
        self.assertTrue(True)
    def test_read_and_print_champion_names_from_csv(self):
        read_and_print_champion_names_from_csv('../results/test.csv', line_start=0, line_end=20)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()