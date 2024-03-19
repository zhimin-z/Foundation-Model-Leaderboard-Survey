import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup
from functools import reduce

url = 'https://financialsupport-open-ita-llm-leaderboard.hf.space'
path_leaderboard = 'data/Open ITA LLM Leaderboard'


def get_json_format_data(script_elements):
    dfs = []
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            df = pd.DataFrame(item['props']['value']['data'], columns=item['props']['value']['headers'])
            df.rename(columns={'model': 'Model', 'model ': 'Model'}, inplace=True)
            dfs.append(df)
    # Merging all DataFrames on the 'Model' column
    df_merged = reduce(lambda left, right: pd.merge(left, right, on='Model', how='outer'), dfs)
    df_merged.to_json(f'{path_leaderboard}/hf.json', orient='records', indent=4)


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
