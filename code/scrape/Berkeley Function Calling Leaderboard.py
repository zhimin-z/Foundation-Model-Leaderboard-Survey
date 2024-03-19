import pandas as pd
import requests
import json
import re
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/Berkeley Function Calling Leaderboard"
leaderboard_names = ['main', 'voting']


def get_json_format_data(script_elements):
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            df = pd.DataFrame(item['props']['value']['data'], columns=item['props']['value']['headers'])
            if 'Rank' in df.columns:
                df.drop(columns=['Rank'], inplace=True)
            df.to_json(f'{path_leaderboard}/hf-{leaderboard_names.pop(0)}.json', orient='records', indent=4)


def extract_model_repo_names(html):
    # This regex pattern looks for the HuggingFace model names in the provided HTML strings.
    # It matches the text after 'https://huggingface.co/' and before the closing double quote.
    pattern = r'https://huggingface.co/([^"]+)'
    matches = re.findall(pattern, html)
    return matches[0]


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    url = 'https://gorilla-llm-berkeley-function-calling-leaderboard.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
