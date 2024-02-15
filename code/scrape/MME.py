import pandas as pd
import re
import os

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
            df.drop(columns=['Rank'], inplace=True)
            for column in df.columns:
                df[column] = df[column].apply(lambda x: x.replace('**', ''))
            dataframes[title.replace(' ', '_')] = df
    return dataframes


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    # Check the latest leaderboards at https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models/blob/Evaluation/README.md
    with open('/Users/jimmy/Downloads/README.md', 'r') as f:
        markdown_content = f.read()
        markdown_content = remove_preceding_content(markdown_content, '## Perception')
        tables_and_titles = extract_tables_and_titles(markdown_content)
        dataframes = markdown_to_dataframe(tables_and_titles)
        for title, df in dataframes.items():
            df.to_json(f'{path_leaderboard}/gh-{title.lower()}.json', orient='records', indent=4)
