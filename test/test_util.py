import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util import config_loader

import unittest

from util.api_requester import create_url
from util.api_requester import LoLRegion, LoLApi, LoLQueue, LoLTier, LoLDivision
from util.api_requester import get_summoner_ids, get_puuid, get_match_ids, get_match
from util.db_manager import init_db, close_db, get_summoner, insert_summoner, check_match_id, update_match_id

config = config_loader.load_config()
key = config['api_keys'][0]

class TestUrlBuilder(unittest.TestCase):
    def test_create_url(self):
        url = create_url(LoLRegion.KOREA, LoLApi.LEAGUE_V4_ENTRIES, queue=LoLQueue.RANKED_SOLO.value, tier=LoLTier.DIAMOND.value, division=LoLDivision.I.value)
        self.assertEqual(url, 'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I')
    def test_create_url_with_query(self):
        url = create_url(LoLRegion.KOREA, LoLApi.LEAGUE_V4_ENTRIES, queue=LoLQueue.RANKED_SOLO.value, tier=LoLTier.DIAMOND.value, division=LoLDivision.I.value, query={"page": 1})
        self.assertEqual(url, 'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1')

class TestGetSummonerIds(unittest.TestCase):
    def test_get_summoner_ids_with_challenger(self):
        ids = get_summoner_ids(key, tier=LoLTier.CHALLENGER)
        self.assertTrue(len(ids) > 0)
    def test_get_summoner_ids_with_grandmaster(self):
        ids = get_summoner_ids(key, tier=LoLTier.GRANDMASTER)
        self.assertTrue(len(ids) > 0)
    def test_get_summoner_ids_with_master(self):
        ids = get_summoner_ids(key, tier=LoLTier.MASTER)
        self.assertTrue(len(ids) > 0)
    def test_get_summoner_ids_with_diamond(self):
        ids = get_summoner_ids(key, tier=LoLTier.DIAMOND, division=LoLDivision.I)
        self.assertTrue(len(ids) > 0)
    def test_get_summoner_ids_with_invalid_key(self):
        ids = get_summoner_ids("invalid_key", tier=LoLTier.CHALLENGER)
        self.assertIsNone(ids)
    def test_get_summoner_ids_with_invalid_tier(self):
        ids = get_summoner_ids(key, tier=LoLTier.IRON)
        self.assertIsNone(ids)

class TestGetPuuid(unittest.TestCase):
    def test_get_puuid(self):
        id = get_puuid(key, "jUwAp2B1Qt4HjXJqT-wA4A3HpwM6XvPE332hi0-ZwH9zpM-h3hfWHiatoA")
        puuid_expected = "8Tvhgmu2DeKWPFHKa_4yMBIGNcaBuhk-xB4Dalna0p7orn4JZigFFMCyotzuK5K8IlyPt-lHhLfLqg"
        self.assertEqual(id, puuid_expected)

class TestGetMatchIds(unittest.TestCase):
    def test_get_match_ids(self):
        ids = get_match_ids(key, "8Tvhgmu2DeKWPFHKa_4yMBIGNcaBuhk-xB4Dalna0p7orn4JZigFFMCyotzuK5K8IlyPt-lHhLfLqg")
        self.assertTrue(len(ids) > 0)
    def test_get_match_ids_with_invalid_key(self):
        ids = get_match_ids("invalid_key", "8Tvhgmu2DeKWPFHKa_4yMBIGNcaBuhk-xB4Dalna0p7orn4JZigFFMCyotzuK5K8IlyPt-lHhLfLqg")
        self.assertIsNone(ids)
    def test_get_match_ids_with_start_time_and_end_time(self):
        ids = get_match_ids(key, "8Tvhgmu2DeKWPFHKa_4yMBIGNcaBuhk-xB4Dalna0p7orn4JZigFFMCyotzuK5K8IlyPt-lHhLfLqg", start_time=1708122899, end_time=1708182000)
        expected_results = [
            "KR_6952430847",
            "KR_6952377180",
            "KR_6952311990",
            "KR_6952279110",
            "KR_6952196159",
            "KR_6952148735",
            "KR_6952104467"
        ]
        self.assertEqual(ids, expected_results)

class TestGetMatchData(unittest.TestCase):
    def test_get_match1(self):
        data = get_match(key, "KR_6952430847")
        self.assertIsNotNone(data)
        expected_results = {
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
        self.assertEqual(data, expected_results)
    def test_get_match2(self):
        data = get_match(key, "KR_6952196159")
        self.assertIsNotNone(data)
        expected_results = {
            "game_version": "14.3.558.8314",
            "game_duration": 2109,
            100: {
                'TOP': 901,
                'JUNGLE': 60,
                'MIDDLE': 111,
                'BOTTOM': 4,
                'UTILITY': 22,
                'win': False,
                'bans': [77, 68, -1, 76, 777]
            },
            200: {
                'TOP': 61,
                'JUNGLE': 64,
                'MIDDLE': 420,
                'BOTTOM': 236,
                'UTILITY': 902,
                'win': True,
                'bans': [78, -1, 43, 200, 268]
            }
        }
        self.assertEqual(data, expected_results)

test_db_path = '../db/test.db'
class TestDbManager(unittest.TestCase):
    def test_init_db(self):
        conn = init_db(path=test_db_path)
        self.assertIsNotNone(conn)
        close_db()
    def test_get_summoner(self):
        init_db(path=test_db_path)
        insert_summoner("test_summonerId", "test_puuid")
        puuid = get_summoner("test_summonerId")
        self.assertEqual(puuid, "test_puuid")
        close_db()
    def test_check_match_id(self):
        init_db(path=test_db_path)
        update_match_id("test_match_id")
        result = check_match_id("test_match_id")
        self.assertTrue(result)
        close_db()
    def test_check_match_id_false(self):
        init_db(path=test_db_path)
        result = check_match_id("test_nothing_id")
        self.assertFalse(result)
        close_db()

if __name__ == '__main__':
    unittest.main()