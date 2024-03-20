import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

url = 'https://seaeval-seaeval-leaderboard.hf.space'
path_leaderboard = 'data/SeaEval'

leaderboard_mapping = {
    'cross_lingual_consistency': ['cross_xquad', 'cross_mmlu', 'cross_logiqa'],
    'culture_reasoning_and_understanding': ['sg_eval', 'us_eval', 'cn_eval', 'ph_eval', 'singlish_to_english_translation'],
    'reasoning': ['mmlu', 'mmlu_full', 'c_eval', 'e_eval_full', 'cmmlu', 'cmmlu_full', 'zbench', 'indommlu'],
    'flores_translation': ['flores_indonesian_to_english_translation', 'flores_vitenamese_to_english_translation', 'flores_chinese_to_english_translation', 'flores_malay_to_english_translation'],
    'emotion_recognition': ['ind_emotion', 'sst2'],
    'dialogue': ['dream', 'samsum', 'dialogsum'],
    'fundamental_nlp': ['ocnli', 'c3', 'cola', 'qqp', 'mnli', 'qnli', 'wnli', 'rte', 'mrpc'],
}


def extract_text(html):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # Extract text from the <a> tag
    text = soup.find('a').get_text()
    return text


def get_leaderboard_names(leaderboard_mapping):
    leaderboard_names = []
    for key, values in leaderboard_mapping.items():
        for value in values:
            for shot in ['zero_shot', 'five_shot']:
                if key == 'cross_lingual_consistency':
                    for split in ['overall', 'language']:
                        leaderboard_names.append(f'{path_leaderboard}/hf-{key}-{value}-{shot}-{split}.json')
                else:
                    leaderboard_names.append(f'{path_leaderboard}/hf-{key}-{value}-{shot}.json')
    return leaderboard_names


def get_json_format_data(script_elements):
    leaderboard_names = get_leaderboard_names(leaderboard_mapping)
    for item in json.loads(str(script_elements[1])[31:-10])['components']:
        if item['type'] == 'dataframe':
            df = pd.DataFrame(item['props']['value']['data'],
                              columns=item['props']['value']['headers'])
            df['Model'] = df['Model'].apply(extract_text)
            df.drop(columns=['Rank'], inplace=True)
            df.to_json(leaderboard_names.pop(0), orient='records', indent=4)


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    get_json_format_data(script_elements)
