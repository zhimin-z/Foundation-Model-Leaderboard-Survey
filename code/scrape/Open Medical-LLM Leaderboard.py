import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/Open Medical-LLM Leaderboard"


def get_json_format_data():
    url = 'https://openlifescienceai-open-medical-llm-leaderboard.hf.space'
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
                        results_json = {"T": results[0], "Model": results[-1], "Average": results[2], "MedMCQA": results[3], "MedQA": results[4], "MMLU Anatomy": results[5], "MMLU Clinical Knowledge": results[6], "MMLU College Biology": results[7], "MMLU College Medicine": results[8], "MMLU Medical Genetics": results[9], "MMLU Professional Medicine": results[10], "PubMedQA": results[11], "Type": results[12], "Architecture": results[13], "Precision": results[14], "Hub License": results[15], "#Params (B)": results[16], "Hub": results[17], "Available on the Hub": results[18], "Model Sha": results[19]}
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