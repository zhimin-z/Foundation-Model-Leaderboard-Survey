import pandas as pd
import requests
import json
import os
import re

from bs4 import BeautifulSoup

path_leaderboard = "data/Open ASR Leaderboard"


def extract_model_repo_names(html):
    # This regex pattern looks for the HuggingFace model names in the provided HTML strings.
    # It matches the text after 'https://huggingface.co/' and before the closing double quote.
    pattern = r'https://huggingface.co/([^"]+)'
    matches = re.findall(pattern, html)
    return matches[0]


def get_json_format_data():
    url = 'https://hf-audio-open-asr-leaderboard.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    json_format_data = json.loads(str(script_elements[1])[31:-10])
    return json_format_data


def get_datas(data):
    for component_index in range(1, 10, 1):  # component_index sometimes changes when they update the space, we can use this "for" loop to avoid changing component index manually
        try:
            result_list = []
            i = 0
            while True:
                try:
                    results = data['components'][component_index]['props']['value']['data'][i]
                    try:
                        results_json = {"Model": extract_model_repo_names(results[0]), "Average WER": results[1], "RTF (1e-3)": results[2], "AMI": results[3], "Earnings22": results[4], "Gigaspeech": results[5], "LS Clean": results[6], "LS Other": results[7], "SPGISpeech": results[8], "Tedlium": results[9], "Voxpopuli": results[10], "Common Voice 9": results[11]}
                    except IndexError:  # Wrong component index, so breaking loop to try next component index. (NOTE: More than one component index can give you some results but we must find the right component index to get all results we want.)
                        break
                    result_list.append(results_json)
                    i += 1
                except IndexError:  # No rows to extract so return the list (We know it is the right component index because we didn't break out of loop on the other exception.)
                    return result_list
        except (KeyError, TypeError):
            continue

    return result_list


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    data = get_json_format_data()
    finished_models = get_datas(data)
    df = pd.DataFrame(finished_models)
    df.to_json(f"{path_leaderboard}/hf.json", orient='records', indent=4)