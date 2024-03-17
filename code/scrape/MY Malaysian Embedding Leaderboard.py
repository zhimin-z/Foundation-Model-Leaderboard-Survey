import pandas as pd
import requests
import json
import os

from bs4 import BeautifulSoup

path_leaderboard = "data/MY Malaysian Embedding Leaderboard"


def get_json_format_data():
    url = 'https://mesolitica-malaysian-embedding-leaderboard.hf.space'
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
                        results_json = {"Model": extract_model_repo_names(results[0]), "Crossref Melayu top-1": results[1], "Crossref Melayu top-3": results[2], "Crossref Melayu top-5": results[3], "Crossref Melayu top-10": results[4], "lom.agc.gov.my top-1": results[5], "lom.agc.gov.my top-3": results[6], "lom.agc.gov.my top-5": results[7], "lom.agc.gov.my top-10": results[8], "b.cari.com.my top-1": results[9], "b.cari.com.my top-3": results[10], "b.cari.com.my top-5": results[11], "b.cari.com.my top-10": results[12], "c.cari.com.my top-1": results[13], "c.cari.com.my top-3": results[14], "c.cari.com.my top-5": results[15], "c.cari.com.my top-10": results[16], "malay-news top-1": results[17], "malay-news top-3": results[18], "malay-news top-5": results[19], "malay-news top-10": results[20], "twitter top-1": results[21], "twitter top-3": results[22], "twitter top-5": results[23], "twitter top-10": results[24]}
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
    # with open(f"{path_leaderboard}/hf.json", 'w') as f:
    #     json.dump(data, f, indent=4)
    finished_models = get_datas(data)
    df = pd.DataFrame(finished_models)
    df.to_json(f"{path_leaderboard}/hf.json", orient='records', indent=4)