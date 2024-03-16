import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/Powered-by-Intel LLM Leaderboard"


def get_json_format_data():
    url = 'https://intel-powered-by-intel-llm-leaderboard.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    json_format_data = json.loads(str(script_elements[1])[31:-10])
    return json_format_data


def get_datas(data):
    for component_index in range(10, 50, 1):  # component_index sometimes changes when they update the space, we can use this "for" loop to avoid changing component index manually
        try:
            result_list = []
            i = 0
            while True:
                try:
                    results = data['components'][component_index]['props']['value']['data'][i]
                    try:
                        results_json = {"Model": results[0], "Average": results[1], "Harware": results[2], "Model Type": results[3], "Precision": results[4], "Size": results[5], "Infrastructure": results[6], "ARC": results[7], "HellaSwag": results[8], "MMLU": results[9], "TruthfulQA": results[10], "Winogrande": results[11], "GSM8K": results[12], "Affiliation": results[13]}
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