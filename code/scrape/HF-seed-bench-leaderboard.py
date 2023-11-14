import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re


def get_json_format_data():
    url = 'https://ailab-cvc-seed-bench-leaderboard.hf.space/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    script_elements = soup.find_all('script')
    json_format_data = json.loads(str(script_elements[1])[31:-10])
    return json_format_data

def extract_model_repo_names(html):
    # This regex pattern looks for the HuggingFace model names in the provided HTML strings.
    # It matches the text after 'https://huggingface.co/' and before the closing double quote.
    pattern = r'https://huggingface.co/([^"]+)'
    matches = re.findall(pattern, html)
    return matches[0]


def get_datas(data):
    for component_index in range(5, 50, 1): # component_index sometimes changes when they update the space, we can use this "for" loop to avoid changing component index manually
        try:
            result_list = []
            i = 0
            while True:
                try:
                    results = data['components'][component_index]['props']['value']['data'][i]
                    # model = extract_model_repo_names(results[1])
                    print(len(results))
                    try:
                        results_json = {"Model Type": results[0], "Model": results[1], "Language Model": results[2], "Avg. All": results[3], "Avg. Img": results[4], "Avg. Video": results[5], "Scene Understanding": results[6], "Instance Identity": results[7], "Instance Attributes": results[8],"Instance Localization": results[9], "Instance Counting": results[10], "Spatial Relation": results[11], "Instance Interaction": results[12], "Visual Reasoning": results[13], "Text Recognition": results[14], "Action Recognition": results[15], "Action Prediction": results[16], "Procedure Understanding": results[17]}                        
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
        df.to_csv("HF-SEED-Bench-Leaderboard.csv", index=False)
        print("Data exported to CSV")

    if args.html:
        df.to_html("HF-SEED-Bench-Leaderboard.html", index=False)
        print("Data exported to HTML")

    if args.json:
        df.to_json("HF-SEED-Bench-Leaderboard-20231110.json", orient='records', indent=4)
        print("Data exported to JSON")

if __name__ == "__main__":
    main()