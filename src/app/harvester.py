import sys
import os
import logging
import random

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util.api_requester import LoLTier, LoLDivision, get_summoner_ids, get_match_ids, get_match
from util.api_requester import get_puuid as get_puuid_from_api
from util.db_manager import get_summoner, insert_summoner, check_match_id, update_match_id
from util.csv_manager import append_to_csv

def harvester(api_key, maximum=1000):
    logging.info("Harvesting started")
    tiers = [LoLTier.CHALLENGER, LoLTier.GRANDMASTER, LoLTier.MASTER, LoLTier.DIAMOND, LoLTier.PLATINUM, LoLTier.GOLD, LoLTier.SILVER, LoLTier.BRONZE, LoLTier.IRON]
    current_index = 0
    while True:
        if current_index == len(tiers):
            current_index = 0
        tier = tiers[current_index]
        harvest(api_key, tier, maximum)
        current_index += 1

def harvest(api_key, tier, maximum=1000):
    logging.info(f"Harvesting {tier} with maximum {maximum} matches.")
    count = 0
    summoners = get_summoners(api_key, tier)
    if summoners is not None:
        for summoner in summoners:
            puuid = get_puuid(api_key, summoner)
            if puuid is not None:
                result = get_matchs_for_puuid(api_key, puuid, tier)
                count += result
            else:
                continue
            if count >= maximum:
                break
    else:
        logging.error(f"Failed to get summoners with tier {tier}")
    logging.info(f"Harvesting {tier} finished with {count} matches.")

def get_summoners(api_key, tier):
    if tier == LoLTier.CHALLENGER or tier == LoLTier.GRANDMASTER or tier == LoLTier.MASTER:
        result = get_summoner_ids(api_key, tier=tier)
        division = None
        page = None
    else:
        division = random.choice([LoLDivision.I, LoLDivision.II, LoLDivision.III, LoLDivision.IV])
        page_max = 500
        page = random.randint(1, page_max)
        result = []
        while len(result) == 0:
            ids = get_summoner_ids(api_key, tier=tier, division=division, page=page)
            if ids is not None:
                result = ids
                break
            else:
                result = []
            page_max /= 2
            page_max = int(page_max)
            page = random.randint(1, page_max)

    logging.info(f"Got {len(result)} summoners with tier {tier} and division {division} from page {page}")
    random.shuffle(result)
    if result is not None:
        return result
    else:
        return None

def get_puuid(api_key, summonerId):
    puuid = get_summoner(summonerId)
    if puuid is not None:
        return puuid
    else:
        puuid = get_puuid_from_api(api_key, summonerId)
        if puuid is not None:
            insert_summoner(summonerId, puuid)
            return puuid
        else:
            return None

def get_matchs_for_puuid(api_key, puuid, tier):
    count = 0
    match_ids = get_match_ids(api_key, puuid)

    if match_ids is None:
        return 0
    
    for match_id in match_ids:
        if check_match_id(match_id):
            continue
        else:
            match = get_match(api_key, match_id)
            if match is not None:
                update_match_id(match_id)
                append_to_csv(match, tier)
                count += 1
            else:
                continue
    return count