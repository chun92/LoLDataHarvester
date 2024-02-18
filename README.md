# LoLDataHarvester

## Overview
LoLDataHarvester is a project dedicated to collecting match datasets from the popular online game League of Legends. The primary objective is to gather data for use in deep learning and other analytical applications. This tool enables researchers and enthusiasts to access a wealth of match information, facilitating studies on game dynamics, player strategies, and champion synergies.

## Usage
To begin collecting your League of Legends match datasets, follow these steps:

1. Create a Riot account at [Riot Developer Portal](https://developer.riotgames.com/).
2. Obtain a Development Key.
3. Alternatively, you can get an API key by registering a product.
4. Update the "api_key" in the `config.json.example` file with your API key and rename the file to `config.json`:
    ```json
    {
        "api_key": "your_api_key"
    }
    ```
5. Install necessary Python packages:
    ```bash
    pip install pandas
    ```
6. Execute the script from the `src/app` directory:
    ```bash
    python app.py
    ```
7. The dataset will be generated in `results/data.csv` in CSV format.
8. The dataset includes the following information:
    ```
    game_version,tier,100.TOP,100.JUNGLE,100.MIDDLE,100.BOTTOM,100.UTILITY,200.TOP,200.JUNGLE,200.MIDDLE,200.BOTTOM,200.UTILITY,game_result,game_duration
    ```
    - `game_version`: The game version, e.g., version 14.3 is stored as 143.
    - `tier`: From 1 (Iron) to 10 (Challenger).
    - The next 10 numbers represent the champion picks for the blue and red teams (top/jg/mid/bot/sup in order).
    - `game_result`: 1 if blue wins, 0 if red wins.
    - `game_duration`: Game duration in seconds.

9. For a human-readable format of the dataset, use `script/print_csv.py`. Example output:
    ```
    0: 143/CHALLENGER      Blue:Pantheon/Hecarim/Ahri/Samira/Maokai        Red:Gragas/Belveth/Yasuo/Xerath/Senna   BlueWin/172
    ```

## Limitations
This project adheres to the personal API rate limits set by Riot:
- 20 requests every 1 second(s)
- 100 requests every 2 minutes(s)

Currently, the focus is on researching champion synergies; therefore, the dataset may not include extensive in-game data. Users interested in more detailed match information are encouraged to fork this repository and adjust it to their needs. The implementation indiscriminately collects datasets across all tiers.

## Future Work
- Obtaining a rate limit exemption for product API.
- Enhancing data collection speed by utilizing multiple API keys.
- Adding arguments to filter datasets by frequency and provide detailed tier segmentation.
