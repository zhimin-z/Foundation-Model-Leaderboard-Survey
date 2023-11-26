import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

from pathlib import Path

path_llm = Path("data/llm")


def get_json_format_data():
    url = 'https://optimum-llm-perf-leaderboard.hf.space/'
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
                    model = extract_model_repo_names(results[0])
                    try:
                        results_json = {"Model": model, "Arch": results[1], "Size": results[2], "Backend": results[3], "Dtype": results[4], "Optimizations": results[5], "Quantization": results[6], "Avg Score (%)": results[7], "Decode Throughput (tokens/s)": results[8],"E2E Throughput (tokens/s)": results[9], "Prefill Latency (s)": results[10], "E2E Latency (s)": results[11], "Allocated Memory (MB)": results[12], "Reserved Memory (MB)": results[13], "Used Memory (MB)": results[14], "Energy (tokens/kWh)": results[15]}                        
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
        df.to_csv(path_llm / "HuggingFace-llm_perf.csv", index=False)
        print("Data exported to CSV")

    if args.html:
        df.to_html(path_llm / "HuggingFace-llm_perf.html", index=False)
        print("Data exported to HTML")

    if args.json:
        df.to_json(path_llm / "HuggingFace-llm_perf.json", orient='records', indent=4)
        print("Data exported to JSON")

if __name__ == "__main__":
    main()