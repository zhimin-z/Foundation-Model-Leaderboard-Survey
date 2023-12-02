from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json
import re

from pathlib import Path

path_llm = Path("data/llm")


def RefineBaseTitle(title, allUpper=False):
    title = title.replace('-', '_')
    if allUpper:
        title = title.upper()
    else:
        title = '_'.join(word.capitalize() for word in title.split('_'))
    return title

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    dataset = 'beir'
    base_url = 'https://paperswithcode.com'
    url = f'{base_url}/dataset/{dataset}'
    driver.get(url)
    
    leaderboard_tables = driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr')
    leaderboard_links = []
    
    for leaderboard in leaderboard_tables:
        text = leaderboard.get_attribute('onclick')
        match = re.findall(r"'(.*?)'", text)[0]
        link = f'{base_url}{match}'
        leaderboard_links.append(link)
    
    for link in leaderboard_links:
        driver.get(link)
        table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
        table = json.loads(table)
        table = pd.DataFrame(table)
        title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
        title = '_'.join(title.lower().replace(f' on {dataset}', '').split())
        table.to_json(path_llm / f'{RefineBaseTitle(dataset, allUpper=True)}-{title}.json', orient='records', indent=4)
                