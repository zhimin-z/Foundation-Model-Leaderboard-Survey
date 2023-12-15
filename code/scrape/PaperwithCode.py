from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json
import re

from pathlib import Path

def dataset_rename(name):
    name = name.lower()
    name = name.replace(' - ', '_')
    name = name.replace('-', '_')
    name = name.replace(' ', '_')
    return name

def file_rename(folder, dataset, title):
    return '_'.join(title.lower().replace(f' on {dataset.lower()}', '').replace(f' on {folder.lower()}', '').split())

folder = ''
dataset = 'LAMBADA'
path_leaderboard = Path(f"data/{folder}") if folder else Path(f"data/{dataset}")

included_links = []

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    leaderboard_links = []
    base_url = 'https://paperswithcode.com'
    
    if included_links:
        for match in included_links:
            link = f'{base_url}/sota/{match}'
            leaderboard_links.append(link)
    else:
        url = f'{base_url}/dataset/{dataset_rename(dataset)}'
        driver.get(url)
        leaderboard_tables = driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr')
        for leaderboard in leaderboard_tables:
            text = leaderboard.get_attribute('onclick')
            match = re.findall(r"'(.*?)'", text)[0]
            link = f'{base_url}{match}'
            leaderboard_links.append(link)
    
    for link in leaderboard_links:
        driver.get(link)
        table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
        if table != '[]':
            table = json.loads(table)
            table = pd.DataFrame(table)
            title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
            title = file_rename(folder, dataset, title)
            table.to_json(path_leaderboard / f'pwc-{title}.json', orient='records', indent=4)
        else:
            table = driver.find_element(By.XPATH, '//script[@id="community-table-data"]').get_attribute("innerText")
            if table != '[]':
                table = json.loads(table)
                table = pd.DataFrame(table)
                title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
                title = file_rename(folder, dataset, title)
                table.to_json(path_leaderboard / f'pwc-{title}.json', orient='records', indent=4)
                