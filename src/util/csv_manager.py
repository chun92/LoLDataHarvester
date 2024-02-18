import pandas as pd
import os
from .api_requester import LoLTier
from .config_loader import get_champion_dict

def lol_tier_to_int(tier):
    if tier == LoLTier.IRON:
        return 1
    elif tier == LoLTier.BRONZE:
        return 2
    elif tier == LoLTier.SILVER:
        return 3
    elif tier == LoLTier.GOLD:
        return 4
    elif tier == LoLTier.PLATINUM:
        return 5
    elif tier == LoLTier.EMERALD:
        return 6
    elif tier == LoLTier.DIAMOND:
        return 7
    elif tier == LoLTier.MASTER:
        return 8
    elif tier == LoLTier.GRANDMASTER:
        return 9
    elif tier == LoLTier.CHALLENGER:
        return 10
    else:
        return 0
    
def int_to_lol_tier_value(tier):
    if tier == 1:
        return LoLTier.IRON.value
    elif tier == 2:
        return LoLTier.BRONZE.value
    elif tier == 3:
        return LoLTier.SILVER.value
    elif tier == 4:
        return LoLTier.GOLD.value
    elif tier == 5:
        return LoLTier.PLATINUM.value
    elif tier == 6:
        return LoLTier.EMERALD.value
    elif tier == 7:
        return LoLTier.DIAMOND.value
    elif tier == 8:
        return LoLTier.MASTER.value
    elif tier == 9:
        return LoLTier.GRANDMASTER.value
    elif tier == 10:
        return LoLTier.CHALLENGER.value
    else:
        return None

def append_to_csv(data_obj, tier, csv_path='../../results/data.csv'):
    game_version = int(''.join(data_obj['game_version'].split('.')[:2]))
    game_result = 1 if data_obj[100]['win'] else 0
    tier_int = lol_tier_to_int(tier)

    data = {
        'game_version': game_version,
        'tier': tier_int,
        '100.TOP': data_obj[100]['TOP'],
        '100.JUNGLE': data_obj[100]['JUNGLE'],
        '100.MIDDLE': data_obj[100]['MIDDLE'],
        '100.BOTTOM': data_obj[100]['BOTTOM'],
        '100.UTILITY': data_obj[100]['UTILITY'],
        '200.TOP': data_obj[200]['TOP'],
        '200.JUNGLE': data_obj[200]['JUNGLE'],
        '200.MIDDLE': data_obj[200]['MIDDLE'],
        '200.BOTTOM': data_obj[200]['BOTTOM'],
        '200.UTILITY': data_obj[200]['UTILITY'],
        'game_result': game_result,
        'game_duration': data_obj['game_duration']
    }
    
    df = pd.DataFrame([data])
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        header = False
    else:
        header = True
    df.to_csv(csv_path, mode='a', index=False, header=header)


def read_and_print_champion_names_from_csv(csv_path, line_start=0, line_end=20):
    df = pd.read_csv(csv_path)
    df_subset = df.iloc[line_start:line_end]
    champion_dict = get_champion_dict()
    for col in ['100.TOP', '100.JUNGLE', '100.MIDDLE', '100.BOTTOM', '100.UTILITY',
                '200.TOP', '200.JUNGLE', '200.MIDDLE', '200.BOTTOM', '200.UTILITY']:
        df_subset[col] = df_subset[col].apply(lambda x: champion_dict[str(x)] if str(x) in champion_dict else "Unknown")

    # 결과 출력
    for index, row in df_subset.iterrows():
        print(f"{index}: {row['game_version']}/{int_to_lol_tier_value(row['tier'])}\tBlue:{row['100.TOP']}/{row['100.JUNGLE']}/{row['100.MIDDLE']}/{row['100.BOTTOM']}/{row['100.UTILITY']}\t"
              f"Red:{row['200.TOP']}/{row['200.JUNGLE']}/{row['200.MIDDLE']}/{row['200.BOTTOM']}/{row['200.UTILITY']}\t"
              f"{'Blue' if row['game_result'] == 1 else 'Red' }Win/{row['game_duration']}")
