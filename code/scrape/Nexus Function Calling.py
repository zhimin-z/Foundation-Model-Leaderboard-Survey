import pandas as pd
import requests
import json
import re
import os

from bs4 import BeautifulSoup

url = 'https://nexusflow-nexus-function-calling-leaderboard.hf.space'
path_leaderboard = "data/Nexus Function Calling"
leaderboard_names = ['overall', 'climate-nested_parallel', 'stack-mostly_single', 'places-nested', 'otx-single', 'virustotal-single', 'vt_multi-nested', 'vt_multi-parallel', 'nvdlibrary-single', 'nvdlibrary_multi-nested']


def get_json_format_data(script_elements):
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            df = pd.DataFrame(item['props']['value']['data'], columns=item['props']['value']['headers'])
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
        
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
