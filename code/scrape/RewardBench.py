import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/RewardBench"
leaderboard_names = ['overall', 'detailed', 'prior_test_set']


def get_json_format_data(script_elements):
    marker = False
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            marker = not marker
            if marker:
                continue
            df = pd.DataFrame(item['props']['value']['data'], columns=item['props']['value']['headers'])
            df['Model'] = df['Model'].apply(lambda x: extract_text(x))
            df.drop(columns=[''], inplace=True)
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


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    url = 'https://allenai-reward-bench.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
