import pandas as pd
import argparse
import requests
import json

from pathlib import Path
from bs4 import BeautifulSoup

path_leaderboard = Path("data/MVBench")


def get_json_format_data():
    url = 'https://opengvlab-mvbench-leaderboard.hf.space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_elements = soup.find_all('script')
    json_format_data = json.loads(str(script_elements[1])[31:-10])
    return json_format_data


def get_datas(data):
    for component_index in range(20, 50, 1): # component_index sometimes changes when they update the space, we can use this "for" loop to avoid changing component index manually
        try:
            result_list = []
            i = 0
            while True:
                try:
                    results = data['components'][component_index]['props']['value']['data'][i]
                    try:
                        results_json = {"Type": results[0], "Model": results[1], "Language Model": results[2], "Avg": results[3], "Action Antonym": results[4], "Action Count": results[5], "Action Localization": results[6], "Action Prediction": results[7], "Action Sequence": results[8], "Character Count": results[9], "Counterfactual Inference": results[10], "Egocentric Navigation": results[11], "Episodic Reasoning": results[12], "Fine grained Action": results[13], "Fine grained Pose": results[14], "Moving Attribute": results[15], "Moving Count": results[16], "Moving Direction": results[17], "Object Existence": results[18], "Object Interaction": results[19], "Object Shuffle": results[20], "Scene Transition": results[21], "State Change": results[22], "Unexpected Action": results[23]}                        
                    except IndexError: # Wrong component index, so breaking loop to try next component index. (NOTE: More than one component index can give you some results but we must find the right component index to get all results we want.)
                        break
                    result_list.append(results_json)
                    i += 1
                except IndexError: # No rows to extract so return the list (We know it is the right component index because we didn't break out of loop on the other exception.)
                    return result_list
        except (KeyError, TypeError):
            continue

    return result_list



def main():
    parser = argparse.ArgumentParser(description="Scrape and export data from the Hugging Face leaderboard")
    parser.add_argument("-csv", action="store_true", help="Export data to CSV")
    parser.add_argument("-html", action="store_true", help="Export data to HTML")
    parser.add_argument("-json", action="store_true", help="Export data to JSON")
    
    args = parser.parse_args()

    data = get_json_format_data()
    finished_models = get_datas(data)
    df = pd.DataFrame(finished_models)

    if not args.csv and not args.html and not args.json:
        args.json = True  # If no arguments are provided, default to JSON export

    if args.csv:
        df.to_csv(path_leaderboard / "hf.csv", index=False)
        print("Data exported to CSV")

    if args.html:
        df.to_html(path_leaderboard / "hf.html", index=False)
        print("Data exported to HTML")

    if args.json:
        df.to_json(path_leaderboard / "hf.json", orient='records', indent=4)
        print("Data exported to JSON")

if __name__ == "__main__":
    main()