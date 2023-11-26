import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

from pathlib import Path

path_llm = Path("data/llm")


def get_json_format_data():
    url = 'https://upstage-open-ko-llm-leaderboard.hf.space/'
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
                    type_of_emoji = data['components'][component_index]['props']['value']['data'][i][0]

                    try:
                        results_json = {"T": type_of_emoji, "Model": results[-1], "Average ⬆️": results[2], "Ko-ARC": results[3], "Ko-HellaSwag": results[4], "Ko-MMLU": results[5], "Ko-TruthfulQA": results[6], "Ko-CommonGen V2": results[7], "Type": results[8], "Precision": results[9], "Hub License": results[10], "#Params (B)": results[11], "Hub ❤️": results[12], "Model Sha": results[13]}                        
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
        df.to_csv(path_llm / "ko-llm-leaderboard.csv", index=False)
        print("Data exported to CSV")

    if args.html:
        df.to_html(path_llm / "ko-llm-leaderboard.html", index=False)
        print("Data exported to HTML")

    if args.json:
        df.to_json(path_llm / "ko-llm-leaderboard.json", orient='records', indent=4)
        print("Data exported to JSON")

if __name__ == "__main__":
    main()