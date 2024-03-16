import pandas as pd
import requests
import os

from bs4 import BeautifulSoup

path_leaderboard = 'data/Multi-modal Leaderboard'
url = "https://opencompass.openxlab.space/utils/OpenVLM.json"

# def preprocess_name(s):
#     s = s.lower().replace(" ", "_")
#     return s


def extract_text_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text()


if __name__ == "__main__":
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)

    response = requests.get(url)
    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the response content as JSON
        data = response.json()
        overall_rows = []
        benchmark_dfs = {}
        for model, details in data['results'].items():
            # Extract META information for reuse
            meta_info = {
                "Model": model,
                "Parameters": details["META"]["Parameters"],
                "Language Model": details["META"]["Language Model"],
                "Vision Model": details["META"]["Vision Model"],
                "Org": details["META"]["Org"],
                "Time": details["META"]["Time"],
                "Verified": details["META"]["Verified"],
                "OpenSource": details["META"]["OpenSource"],
                "URL": details["META"]["Method"][1]
            }

            # Initialize the row for overall evaluation
            overall_row = meta_info.copy()

            # Iterate through each benchmark
            for benchmark_name, benchmark_details in details.items():
                # Exclude the META section
                if benchmark_name == "META":
                    continue

                # Update overall_row for the overall CSV
                overall_row[benchmark_name] = benchmark_details.get(
                    "Overall", "")
                # Prepare the benchmark-specific row, adding all benchmark details
                benchmark_row = meta_info.copy()
                benchmark_row.update(benchmark_details)

                # Append the row to the appropriate list in benchmark_dfs
                if benchmark_name not in benchmark_dfs:
                    # Start a new list for this benchmark
                    benchmark_dfs[benchmark_name] = [benchmark_row]
                else:
                    benchmark_dfs[benchmark_name].append(benchmark_row)

                overall_rows.append(overall_row)

        df_overall = pd.DataFrame(overall_rows)
        df_overall.to_json(
            f'{path_leaderboard}/iw-main.json', orient='records', indent=4)

        # Convert each benchmark-specific list to a DataFrame and save as CSV
        benchmark_file_paths_merged = {}
        for benchmark_name, benchmark_rows in benchmark_dfs.items():
            df_benchmark = pd.DataFrame(benchmark_rows)
            df_benchmark.to_json(
                f'{path_leaderboard}/iw-{benchmark_name}.json', orient='records', indent=4)
    else:
        print(f"Failed to fetch the data. Status code: {response.status_code}")
