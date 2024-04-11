import pandas as pd
import requests
import json
import os
import re

from bs4 import BeautifulSoup

path_leaderboard = 'data/WildVision Arena Leaderboard'
leaderboard_names = ['full', 'arena']


def get_json_format_data(script_elements):
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            columns = [filter_string(column) for column in item['props']['value']['headers']]
            df = pd.DataFrame(item['props']['value']['data'], columns=columns)
            df['Model'] = df['Model'].apply(lambda x: extract_text(x))
            if 'Rank' in df.columns:
                df.drop(columns=['Rank'], inplace=True)
            df.to_json(f'{path_leaderboard}/hf-{leaderboard_names.pop(0)}.json', orient='records', indent=4)


def extract_text(text):
    try:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        # Extract text from the <a> tag
        text = soup.find('a').get_text()
    except:
        pass
    return text

def filter_string(text):
    regex_pattern = r'🤖|⭐|📚|📊|⚔️'
    filtered_string = re.sub(regex_pattern, '', text)
    return filtered_string.strip()

if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    url = 'https://edde06e8ec17cea720.gradio.live'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
