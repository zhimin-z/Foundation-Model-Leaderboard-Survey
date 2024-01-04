import pandas as pd
import json

from bs4 import BeautifulSoup

path_leaderboard = 'data/(C)MTEB'


def preprocess_name(s):
    s = s.lower().replace(" ", "_")
    return s


def extract_text_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text()


# Check the dataset from https://github.com/AI-Northstar-Tech/mteb-info/blob/main/data/data.json
with open('/Users/jimmy/Downloads/data.json', 'r') as f:
    data = json.load(f)
    for group in data['table']:
        group_name = preprocess_name(group['name'])
        for table in group['table']:
            table_name = preprocess_name(table['name'])
            df = pd.DataFrame(table['data'], columns=table['headers'])
            df['Model'] = df['Model'].apply(extract_text_from_html)
            df.to_json(
                f'{path_leaderboard}/hf-{group_name}-{table_name}.json', orient='records', indent=4)
