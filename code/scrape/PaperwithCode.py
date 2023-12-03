from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json
import re

from pathlib import Path

path_llm = Path("data/llm")

included_links = ['image-classification-on-imagenet', 'self-supervised-image-classification-on', 'image-classification-on-imagenet-real', 'image-classification-on-imagenet-v2', 'domain-generalization-on-imagenet-r', 'zero-shot-transfer-image-classification-on-1', 'zero-shot-transfer-image-classification-on-3', 'zero-shot-transfer-image-classification-on-5', 'zero-shot-transfer-image-classification-on-4']


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

    leaderboard_links = []
    dataset = 'imagenet'
    base_url = 'https://paperswithcode.com'
    url = f'{base_url}/dataset/{dataset}'
    driver.get(url)
    
    if included_links:
        for match in included_links:
            link = f'{base_url}/sota/{match}'
            leaderboard_links.append(link)
    else:
        leaderboard_tables = driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr')
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
                