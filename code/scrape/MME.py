import pandas as pd
import re

path_leaderboard = "data/MME"

def remove_preceding_content(original_string, target_substring):
    # Find the position of the target substring
    position = original_string.find(target_substring)

    # If the substring is found, return the string from that position onwards
    if position != -1:
        return original_string[position:]
    else:
        # If the substring is not found, return the original string
        return original_string

# # Sample markdown content (replace this with the actual markdown file reading)
# markdown_content = """
# ### Text Translation

# | Rank | Model | Version | Score |
# | :--: | :--: | :--: | :--: |
# | 🏅️ | [Qwen-VL-Plus](https://help.aliyun.com/zh/dashscope/developer-reference/vl-plus-quick-start) | [-](https://help.aliyun.com/zh/dashscope/developer-reference/vl-plus-quick-start) | 185.00 |
# | 🥈 | [Qwen-VL-Chat](https://github.com/QwenLM/Qwen-VL/) | [Qwen-7B](https://github.com/QwenLM/Qwen-VL) | 147.50 |
# | 🥉 | [Gemini Pro](https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf) | [-](https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf) | 145.00 |

# ### Code Reasoning

# | Rank | Model | Version | Score |
# | :--: | :--: | :--: | :--: |
# | 🏅️ | [GPT-4V](https://cdn.openai.com/papers/GPTV_System_Card.pdf) | [-](https://cdn.openai.com/papers/GPTV_System_Card.pdf) | 170.00 |
# | 🥈 | [WeMM](https://github.com/scenarios/WeMM) | [InternLM-7B](https://github.com/scenarios/WeMM) | 117.50 |
# | 🥉 | [LLaMA-Adapter V2](https://arxiv.org/pdf/2304.15010.pdf) | [LLaMA-Adapter-v2.1-7B](https://github.com/OpenGVLab/LLaMA-Adapter/tree/main/llama_adapter_v2_multimodal7b) | 90.00 |
# """

def extract_tables_and_titles(markdown_text):
    tables = []
    current_table = []
    current_title = ""
    in_table = False
    header_captured = False

    for line in markdown_text.split('\n'):
        if line.strip().startswith('##'):
            if current_table:
                tables.append((current_title, current_table))
                current_table = []
            current_title = line.strip('# ').strip()
            in_table = False
            header_captured = False
        elif line.strip().startswith('|') and '---' not in line:
            if not header_captured and not in_table:
                current_table.append(line.strip('| \n'))
                header_captured = True
            elif in_table:
                current_table.append(line.strip('| \n'))
            in_table = True
        elif in_table and not line.strip().startswith('|'):
            in_table = False
            tables.append((current_title, current_table))
            current_table = []

    if current_table:
        tables.append((current_title, current_table))

    return tables

def clean_table(table):
    cleaned_table = []
    for row in table:
        # Remove markdown link syntax, keep the link text only
        row = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', row)
        # Split row into columns
        columns = [col.strip() for col in row.split('|')]
        cleaned_table.append(columns)
    return cleaned_table

def markdown_to_dataframe(tables):
    dataframes = {}
    for title, table in tables:
        if table:  # Check if table is not empty
            # Clean the table
            cleaned_table = clean_table(table)
            # Convert to DataFrame
            df = pd.DataFrame(cleaned_table[1:], columns=cleaned_table[0])
            dataframes[title.replace(' ', '_')] = df
    return dataframes

with open('/Users/jimmy/Downloads/README.md', 'r') as f:
    markdown_content = f.read()
    markdown_content = remove_preceding_content(markdown_content, '## Perception')
    tables_and_titles = extract_tables_and_titles(markdown_content)
    dataframes = markdown_to_dataframe(tables_and_titles)

    for title, df in dataframes.items():
        df.to_json(f'{path_leaderboard}/gh-{title.lower()}', orient='records', indent=4)
        print(f"Saved '{title}'")
