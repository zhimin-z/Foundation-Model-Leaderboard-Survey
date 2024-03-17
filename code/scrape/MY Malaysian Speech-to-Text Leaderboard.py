import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/MY Malaysian Speech-to-Text Leaderboard"


def get_json_format_data():
    url = 'https://mesolitica-malaysian-stt-leaderboard.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    json_format_data = json.loads(str(script_elements[1])[31:-10])
    return json_format_data


def extract_model_repo_names(repo):
    if ']' in repo and '[' in repo:
        return repo.split(']')[0].split('[')[1]
    return repo


def get_datas(data):
    for component_index in range(1, 10, 1):  # component_index sometimes changes when they update the space, we can use this "for" loop to avoid changing component index manually
        try:
            result_list = []
            i = 0
            while True:
                try:
                    results = data['components'][component_index]['props']['value']['data'][i]
                    try:
                        results_json = {"Model": results[0], "model size FP16 (MB)": results[1], "Malaya-Speech test CER": results[2], "Malaya-Speech test WER": results[3], "Fleurs MY-MS CER": results[4], "Fleurs MY-MS WER": results[5], "IMDA TTS CER": results[6], "IMDA TTS WER": results[7]}
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