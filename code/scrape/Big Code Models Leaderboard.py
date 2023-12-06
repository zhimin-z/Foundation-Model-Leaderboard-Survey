import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

from pathlib import Path

path_leaderboard = Path("data/Big Code Models Leaderboard")


def get_json_format_data():
    url = 'https://bigcode-bigcode-models-leaderboard.hf.space/'
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
    for component_index in range(10, 50, 1): # component_index sometimes changes when they update the space, we can use this "for" loop to avoid changing component index manually
        try:
            result_list = []
            i = 0
            while True:
                try:
                    results = data['components'][component_index]['props']['value']['data'][i]
                    model = extract_model_repo_names(results[1])
                    try:
                        results_json = {"T": results[0], "Model": model, "Win Rate": results[2], "Throughput (token\/s)": results[3], "Seq_length": results[5], "#Languages": results[6], "humaneval-python": results[7], "java": results[8],"javascript": results[9], "cpp": results[10], "php": results[11], "julia": results[12], "d": results[13], "Average score": results[14], "lua": results[15], "r": results[16], "racket": results[17], "rust": results[18], "swift": results[19], "Throughput (token\/s) bs=50": results[20], "Peak Memory (MB)": results[21], "Link": results[23], 'Submission PR': results[24]}                        
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
        df.to_csv(path_leaderboard / "all.csv", index=False)
        print("Data exported to CSV")

    if args.html:
        df.to_html(path_leaderboard / "all.html", index=False)
        print("Data exported to HTML")

    if args.json:
        df.to_json(path_leaderboard / "all.json", orient='records', indent=4)
        print("Data exported to JSON")

if __name__ == "__main__":
    main()