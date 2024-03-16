import pandas as pd
import requests
import os

from bs4 import BeautifulSoup

path_leaderboard = 'data/Multi-modal Leaderboard'
url = "https://opencompass.openxlab.space/utils/OpenVLM.json"

def preprocess_name(s):
    s = s.lower().replace(" ", "_")
    return s


def extract_text_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text()


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    response = requests.get(url)
    # Checking if the request was successful
    if response.status_code == 200:
    # Parsing the response content as JSON
        data = response.json()
        for group in data['table']:
            group_name = preprocess_name(group['name'])
            for table in group['table']:
                table_name = preprocess_name(table['name'])
                df = pd.DataFrame(table['data'], columns=table['headers'])
                df['Model'] = df['Model'].apply(extract_text_from_html)
                df.to_json(f'{path_leaderboard}/iw-{group_name}-{table_name}.json', orient='records', indent=4)
    else:
        print(f"Failed to fetch the data. Status code: {response.status_code}")

