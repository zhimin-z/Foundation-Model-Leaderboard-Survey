import pandas as pd
import json
import re
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

def file_rename(title):
    title = title.lower()
    title = title.replace(',', '_').replace('/', '_').replace('-', '_').replace(':', '_').replace(' ', '_')
    return title

bloom = False
dataset = ''
path_leaderboard = 'data/CoNLL'
included_leaderboards = ['semantic-role-labeling-on-conll12', 'semantic-role-labeling-on-conll05-brown', 'semantic-role-labeling-on-conll05-wsj', 'coreference-resolution-on-conll12', 'joint-entity-and-relation-extraction-on-2', 'named-entity-recognition-on-conll03', 'relation-extraction-on-conll04', 'coreference-resolution-on-conll-2012', 'named-entity-recognition-ner-on-conll-2003']

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)
    
    leaderboard_links = []
    community_indicator = ''
    base_url = 'https://paperswithcode.com'
    
    if dataset:
        url = f'{base_url}/dataset/{dataset}'
        driver.get(url)
        for leaderboard in driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr'):
            if bloom:
                if 'bloom' not in driver.execute_script("return arguments[0].innerText;", leaderboard):
                    continue
            text = leaderboard.get_attribute('onclick')
            match = re.findall(r"'(.*?)'", text)[0]
            link = f'{base_url}{match}'
            leaderboard_links.append(link)
    else:
        for match in included_leaderboards:
            link = f'{base_url}/sota/{match}'
            leaderboard_links.append(link)
    
    for link in leaderboard_links:
        driver.get(link)
        table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
        if table != '[]':
            table = json.loads(table)
            table = pd.DataFrame(table)
            table = table.rename(columns={'method': 'Model'})
            title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
            title = file_rename(title)
            table.to_json(f'{path_leaderboard}/pwc-{title}.json', orient='records', indent=4)
            community_indicator = 'community-'
        table = driver.find_element(By.XPATH, '//script[@id="community-table-data"]').get_attribute("innerText")
        if table != '[]':
            table = json.loads(table)
            table = pd.DataFrame(table)
            table = table.rename(columns={'method': 'Model'})
            title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
            title = file_rename(title)
            table.to_json(f'{path_leaderboard}/pwc-{community_indicator}{title}.json', orient='records', indent=4)
    
    driver.quit()