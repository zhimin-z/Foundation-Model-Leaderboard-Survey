import pandas as pd
import requests
import json
import os
import re

from bs4 import BeautifulSoup

path_leaderboard = "data/Open PL LLM Leaderboard"


def get_json_format_data():
    url = 'https://speakleash-open-pl-llm-leaderboard.hf.space'
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
                        results_json = {"T": results[0], "Model": results[-1], "n-shot": results[2], "Average": results[3], "Avg g": results[4], "Avg mc": results[5], "belebele_pol_Latn": results[6], "polemo2-in_g": results[7], "polemo2-in_mc": results[8], "polemo2-out_g": results[9], "polemo2-out_mc": results[10], "8tags_mc": results[11], "8tags_g": results[12], "belebele_g": results[13], "dyk_mc": results[14], "dyk_g": results[15], "ppc_mc": results[16], "ppc_g": results[17], "psc_mc": results[18], "psc_g": results[19], "cbd_mc": results[20], "cbd_g": results[21], "klej_ner_mc": results[22], "klej_ner_g": results[23], "Type": results[24], "Architecture": results[25], "Precision": results[26], "Hub License": results[27], "Lang": results[28], "#Params (B)": results[29], "Hub": results[30], "Available on the Hub": results[31], "Model Sha": results[32]}
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