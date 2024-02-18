import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util.config_loader import get_latest_game_version, get_champion_dict, get_latest_game_version_from_server, get_champion_list_from_server, extract_key_id_mapping

import unittest

class TestConfig(unittest.TestCase):
    def test_get_latest_game_version_from_server(self):
        version = get_latest_game_version_from_server()
        self.assertIsNotNone(version)

    def test_get_champion_list_from_server(self):
        version = get_latest_game_version_from_server()
        champions = get_champion_list_from_server(version)
        self.assertIsNotNone(champions)
    
    def test_extract_key_id_mapping(self):
        version = get_latest_game_version_from_server()
        champions = get_champion_list_from_server(version)
        mapping = extract_key_id_mapping(champions)
        self.assertIsNotNone(mapping)
    
    def test_get_latest_game_version(self):
        version = get_latest_game_version()
        self.assertIsNotNone(version)
    
    def test_get_champion_dict(self):
        champions = get_champion_dict()
        self.assertIsNotNone(champions)

if __name__ == '__main__':
    unittest.main()