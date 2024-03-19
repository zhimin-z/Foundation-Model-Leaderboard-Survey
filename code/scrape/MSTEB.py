import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

url = 'https://clibrain-spanish-embeddings-leaderboard.hf.space'
path_leaderboard = "data/MSTEB"
leaderboard_names = ['overall', 'classification', 'sts', 'clustering', 'retrieval']


def get_json_format_data(script_elements):
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            df = pd.DataFrame(item['props']['value']['data'], columns=item['props']['value']['headers'])
            df.rename(columns={'Model name': 'Model'}, inplace=True)
            df.to_json(f'{path_leaderboard}/hf-{leaderboard_names.pop(0)}.json', orient='records', indent=4)


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
