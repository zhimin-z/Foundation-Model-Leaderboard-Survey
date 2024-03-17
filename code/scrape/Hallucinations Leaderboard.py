import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/Hallucinations Leaderboard"


def get_json_format_data():
    url = 'https://hallucinations-leaderboard-leaderboard.hf.space'
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
                        results_json = {"T": results[0], "Model": results[-1], "NQ Open/EM": results[2], "TriviaQA/EM": results[3], "TruthQA MC1/Acc": results[4], "TruthQA MC2/Acc": results[5], "TruthQA Gen/ROUGE": results[6], "XSum/ROUGE": results[7], "XSum/factKB": results[8], "XSum/BERT-P": results[9], "CNN-DM/ROUGE": results[10], "CNN-DM/factKB": results[11], "CNN-DM/BERT-P": results[12], "RACE/Acc": results[13], "SQUaDv2/EM": results[14], "MemoTrap/Acc": results[15], "IFEval/Acc": results[16], "FaithDial/Acc": results[17], "HaluQA/Acc": results[18], "HaluSumm/Acc": results[19], "HaluDial/Acc": results[20], "FEVER/Acc": results[21], "TrueFalse/Acc": results[22], "Type": results[13], "Architecture": results[24], "Precision": results[25], "Hub License": results[26], "#Params (B)": results[27], "Hub": results[28], "Available on the hub": results[29], "Model sha": results[30]}
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