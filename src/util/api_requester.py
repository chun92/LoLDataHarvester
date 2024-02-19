import time
import requests
import logging

from enum import Enum

class LoLApi(Enum):
    LEAGUE_V4_CHALLENGER = "/lol/league/v4/challengerleagues/by-queue/{queue}"
    LEAGUE_V4_GRANDMASTER = "/lol/league/v4/grandmasterleagues/by-queue/{queue}"
    LEAGUE_V4_MASTER = "/lol/league/v4/masterleagues/by-queue/{queue}"
    LEAGUE_V4_ENTRIES = "/lol/league/v4/entries/{queue}/{tier}/{division}"
    SUMMONER_V4_BY_SUMMONERID = "/lol/summoner/v4/summoners/{encryptedSummonerId}"
    MATCH_V5_MATCHLIST = "/lol/match/v5/matches/by-puuid/{puuid}/ids"
    MATCH_V5_MATCH = "/lol/match/v5/matches/{matchId}"

class LoLQueue(Enum):
    RANKED_SOLO = "RANKED_SOLO_5x5"
    RANKED_FLEX_SR = "RANKED_FLEX_SR"
    RANKED_FLEX_TT = "RANKED_FLEX_TT"

class LoLRegion(Enum):
    BRAZIL = "br1"
    EUROPE_NORTH_EAST = "eun1"
    EUROPE_WEST = "euw1"
    JAPAN = "jp1"
    KOREA = "kr"
    LATIN_AMERICA_NORTH = "la1"
    LATIN_AMERICA_SOUTH = "la2"
    NORTH_AMERICA = "na1"
    OCEANIA = "oc1"
    Philippines = "ph2"
    Singapore = "sg2"
    Thailand = "th2"
    Turkey = "tr1"
    Taiwan = "tw2"
    VIETNAM = "vn2"
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"
    SEA = "sea"

class LoLTier(Enum):
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    EMERALD = "EMERALD"
    DIAMOND = "DIAMOND"
    MASTER = "MASTER"
    GRANDMASTER = "GRANDMASTER"
    CHALLENGER = "CHALLENGER"

class LoLDivision(Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"

def create_url(region, api, query={},**kwargs):
    url = f"https://{region.value}.api.riotgames.com{api.value}"
    url = url.format(**kwargs)
    if query:
        url += "?"
        for key, value in query.items():
            url += f"{key}={value}&"
        url = url[:-1]

    return url


class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.requests = []

    def wait(self):
        now = time.time()
        while self.requests and self.requests[0] < now - self.period:
            self.requests.pop(0)

        if len(self.requests) >= self.max_requests:
            sleep_time = self.period - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.requests.append(time.time())

rate_limiter = RateLimiter(100, 120)  # 100 requests per 120 seconds


def send_request(url, api_key, max_retries=3, backoff_factor=2):
    rate_limiter.wait()
    headers = {"X-Riot-Token": api_key}
    retries = 0
    
    while retries <= max_retries:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                logging.warning(f"Rate limit exceeded. Retrying... ({retries+1}/{max_retries})")
                retries += 1
                time.sleep(backoff_factor ** retries)
            else:
                if response.status_code == 200:
                    logging.info(f"Request to {url} succeeded with status code {response.status_code}.")
                else:
                    logging.error(f"Request to {url} failed with status code {response.status_code}.")
                return response.status_code, response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            return None, None
    logging.error(f"Max retries exceeded for {url}")
    return None, None
    
def get_summoner_ids(api_key, region=LoLRegion.KOREA, queue=LoLQueue.RANKED_SOLO, tier=None, division=None, page=1):
    if tier == LoLTier.CHALLENGER:
        url = create_url(region, LoLApi.LEAGUE_V4_CHALLENGER, queue=queue.value)
    elif tier == LoLTier.GRANDMASTER:
        url = create_url(region, LoLApi.LEAGUE_V4_GRANDMASTER, queue=queue.value)
    elif tier == LoLTier.MASTER:
        url = create_url(region, LoLApi.LEAGUE_V4_MASTER, queue=queue.value)
    else:
        if not tier or not division:
            logging.error("Tier and division must be specified.")
            return None
        url = create_url(region, LoLApi.LEAGUE_V4_ENTRIES, queue=queue.value, tier=tier.value, division=division.value, query={"page": page})
    status_code, response = send_request(url, api_key)

    if status_code == 200:
        if not response:
            return None
        if tier == LoLTier.CHALLENGER or tier == LoLTier.GRANDMASTER or tier == LoLTier.MASTER:
            entries = response["entries"]
        else:
            entries = response
        results = []
        for entry in entries:
            encrypted_summoner_id = entry["summonerId"]
            results.append(encrypted_summoner_id)
        logging.info(f"Retrieved {len(results)} summoner ids.")
        return results
    else:
        logging.error(f"Failed to retrieve summoner ids with status code {status_code}.")
        return None
    
def get_puuid(api_key, encrypted_summoner_id, region=LoLRegion.KOREA):
    url = create_url(region, LoLApi.SUMMONER_V4_BY_SUMMONERID, encryptedSummonerId=encrypted_summoner_id)
    status_code, response = send_request(url, api_key)
    if status_code == 200:
        logging.info(f"Retrieved puuid for summoner {encrypted_summoner_id}.")
        return response["puuid"]
    else:
        logging.error(f"Failed to retrieve puuid for summoner {encrypted_summoner_id} with status code {status_code}.")
        return None

def get_match_ids(api_key, puuid, region=LoLRegion.ASIA, start=0, count=20, start_time=None, end_time=None, queue=420, type="ranked"):
    query = {
        "start": start,
        "count": count,
        "queue": queue,
        "type": type
    }
    if start_time:
        query["startTime"] = start_time
    if end_time:
        query["endTime"] = end_time

    url = create_url(region, LoLApi.MATCH_V5_MATCHLIST, puuid=puuid, query=query)
    
    status_code, response = send_request(url, api_key)
    if status_code == 200:
        logging.info(f"Retrieved {len(response)} match ids for summoner {puuid}.")
        return response
    else:
        logging.error(f"Failed to retrieve match ids for summoner {puuid} with status code {status_code}.")
        return None

def get_match(api_key, match_id, region=LoLRegion.ASIA):
    url = create_url(region, LoLApi.MATCH_V5_MATCH, matchId=match_id)
    status_code, response = send_request(url, api_key)
    if status_code == 200:
        logging.info(f"Retrieved match {match_id}.")

        try:
            if "endOfGameResult" not in response["info"]:
                logging.warn(f"Match {match_id} has no end of game result.")
            else:
                end_of_game_result = response["info"]["endOfGameResult"]
                if end_of_game_result != "GameComplete":
                    logging.warn(f"Match {match_id} is not complete.")
                    return None
            results = {}

            game_version = response["info"]["gameVersion"]
            game_duration = response["info"]["gameDuration"]

            results["game_version"] = game_version
            results["game_duration"] = game_duration

            participants = response["info"]["participants"]
            teams = response["info"]["teams"]

            for team in teams:
                bans = team["bans"]
                result_bans = []
                for ban in bans:
                    result_bans.append(ban["championId"])
                results[team["teamId"]] = {
                    "win": team["win"],
                    "bans": result_bans
                }
            
            for participant in participants:
                champion_id = participant["championId"]
                team_id = participant["teamId"]
                team_position = participant["teamPosition"]
                results[team_id][team_position] = champion_id
            
            if (results[100]['TOP'] is None or 
                results[100]['JUNGLE'] is None or
                results[100]['MIDDLE'] is None or
                results[100]['BOTTOM'] is None or
                results[100]['UTILITY'] is None or
                results[200]['TOP'] is None or
                results[200]['JUNGLE'] is None or
                results[200]['MIDDLE'] is None or
                results[200]['BOTTOM'] is None or
                results[200]['UTILITY'] is None):
                logging.error(f"Match {match_id} is missing participant information.")
                return None
            
            if (results[100]["bans"] is None or results[200]["bans"] is None):
                logging.error(f"Match {match_id} is missing ban information.")
                return None
            
            logging.info(f"Match {match_id} successfully parsed.")
            return results
        except:
            logging.error(f"Failed to parse match {match_id}.")
            return None
    else:
        logging.error(f"Failed to retrieve match {match_id} with status code {status_code}.")
        return None