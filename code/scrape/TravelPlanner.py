import pandas as pd
import requests
import json

from pathlib import Path
from bs4 import BeautifulSoup

path_leaderboard = Path("data/TravelPlanner")
leaderboard_names = ['Validation | Two-Stage', 'Validation | Sole-Planning', 'Test | Two-Stage', 'Test | Sole-Planning']


def preprocess_name(name):
    name = name.lower()
    name = name.replace('-', '_')
    name = name.replace(' | ', '_')
    return name


def get_json_format_data(script_elements):
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            columns = item['props']['value']['headers']
            print(columns)
            data = item['props']['value']['data']
            df = pd.DataFrame(data, columns=columns)
            df.to_json(
                path_leaderboard / f'hf-{preprocess_name(leaderboard_names.pop(0))}.json', orient='records', indent=4)


if __name__ == "__main__":
    url = 'https://osunlp-travelplannerleaderboard.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
