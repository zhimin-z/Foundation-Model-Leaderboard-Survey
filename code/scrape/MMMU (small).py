from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import pandas as pd
import json
import re

path_leaderboard = "data/MMMU"


def camel_to_snake(name):
    # Insert an underscore before each uppercase letter (that is not at the start of the string) and convert to lowercase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def space_to_underline(name):
    return name.strip().replace(' ', '_').lower()


def process_script_content(script_content, pattern):
    match = re.search(pattern, script_content, re.DOTALL)
    json_str = match.group(1)
    json_str = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_str)
    json_str = json_str.replace("'", '"')
    data = json.loads(json_str)
    return data


if __name__ == '__main__':
    # Check the leaderboards from https://github.com/MMMU-Benchmark/mmmu-benchmark.github.io/blob/main/index.html
    absolute_html_file_path = '/Users/jimmy/Downloads/index.html'
    with open(absolute_html_file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    script_content = soup.find('body').find('script').string
    for table in soup.find_all('div', class_='chart-item'):
        table_name = table.find('canvas').get('id').replace('chart', 'data')
        data = process_script_content(
            script_content, pattern=rf'const {table_name}\s*=\s*(\{{.*?\}});')
        df = pd.DataFrame([data['datasets'][0]['data']],
                          columns=data['labels'])
        df.to_json(f"{path_leaderboard}/gh-image_type-{camel_to_snake(table_name.replace('data_', ''))}.json",
                   orient='records', indent=4)

    driver = uc.Chrome()
    driver.implicitly_wait(5)
    driver.get('https://mmmu-benchmark.github.io')
    script = """
    // This script extracts the labels and datasets from the Chart configuration
    const chart = difficulty_level_chart.config.data; // Assuming difficulty_level_chart is accessible
    return {
        labels: chart.labels,
        datasets: chart.datasets
    };
    """
    data = driver.execute_script(script)

    dataframes = []
    for index, label in enumerate(data["labels"]):
        rows = []
        for dataset in data["datasets"]:
            row = {"label": dataset["label"], "data": dataset["data"][index]}
            rows.append(row)
        df = pd.DataFrame(rows)
        df.to_json(f'{path_leaderboard}/gh-difficulty_level-{label.lower()}.json',
                   orient='records', indent=4)

    button = driver.find_element(By.XPATH, '//button[@id="toggleButton"]')
    table = driver.find_element(By.XPATH, '//table[@class="js-sort-table"]')

    column_names = ['Model']
    for column in table.find_elements(By.XPATH, './/thead/tr/td'):
        if 'Reset' == column.text:
            continue
        column_names.append(column.text)

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for value in row.find_elements(By.XPATH, './/td'):
            values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.to_json(
        f'{path_leaderboard}/gh-{space_to_underline(button.text.split("Leaderboard")[0])}.json', orient='records', indent=4)

    button.click()
    table = driver.find_element(By.XPATH, '//table[@class="js-sort-table"]')

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for value in row.find_elements(By.XPATH, './/td'):
            values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.to_json(
        f'{path_leaderboard}/gh-{space_to_underline(button.text.split("Leaderboard")[0])}.json', orient='records', indent=4)
