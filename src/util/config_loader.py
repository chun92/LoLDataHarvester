import json
import os
import requests
import time
import logging

def load_config(filename='../../key/config.json'):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)
    
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

latest_version_cache = None
champion_dict_cache = None
last_update_time = 0

def get_latest_game_version():
    global latest_version_cache
    update_from_server()
    return latest_version_cache

def get_champion_dict():
    global champion_dict_cache
    update_from_server()
    return champion_dict_cache

def update_from_server():
    global latest_version_cache, last_update_time, champion_dict_cache
    
    time_diff = time.time() - last_update_time
    
    if time_diff > 86400 or champion_dict_cache is None:
        latest_version_cache = get_latest_game_version_from_server()
        last_update_time = time.time()
        champions = get_champion_list_from_server(latest_version_cache)
        champion_dict_cache = extract_key_id_mapping(champions)
        logging.info(f"Updated champion list from server. Latest version: {latest_version_cache}")
    else:
        return

def get_latest_game_version_from_server(url='https://ddragon.leagueoflegends.com/api/versions.json'):
    try:
        response = requests.get(url)
        response.raise_for_status()
        versions = response.json()
        return versions[0]
    except requests.HTTPError as e:
        print(f"Error fetching versions: {e}")
        return None

def get_champion_list_from_server(version, url='http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'):
    try:
        url = url.format(version)
        response = requests.get(url)
        response.raise_for_status()
        champions = response.json()
        return champions
    except requests.HTTPError as e:
        print(f"Error fetching champions: {e}")
        return None
    
def extract_key_id_mapping(champion_json):
    key_id_mapping = {}
    
    for champ_key, champ_data in champion_json['data'].items():
        champ_id = champ_data['id']
        champ_key = champ_data['key']
        key_id_mapping[champ_key] = champ_id
    
    return key_id_mapping