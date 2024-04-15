import pandas as pd
import json
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

def file_rename(title):
    title = title.lower()
    title = title.replace(',', '_').replace('/', '_').replace('-', '_').replace(':', '_').replace(' ', '_')
    return title

dataset = '3dpw'
path_leaderboard = 'data/3dpw'
included_leaderboards = []
use_bloom_only = False

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)
    
    leaderboard_urls = []
    base_url = 'https://paperswithcode.com'
    
    if dataset:
        url = f'{base_url}/dataset/{dataset}'
        driver.get(url)
        for leaderboard in driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr'):
            if use_bloom_only:
                if 'bloom' not in driver.execute_script("return arguments[0].innerText;", leaderboard):
                    continue
            url = leaderboard.find_element(By.XPATH, './/td[1]/a').get_attribute("href")
            leaderboard_urls.append(url)
    else:
        for suffix in included_leaderboards:
            url = f'{base_url}/sota/{suffix}'
            leaderboard_urls.append(url)
    
    for url in leaderboard_urls:
        driver.get(url)
        
        table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
        table = json.loads(table)
        if table:
            table = pd.DataFrame(table)
            table = table.rename(columns={'method': 'Model'})
            title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
            title = file_rename(title)
            table.to_json(f'{path_leaderboard}/pwc-{title}.json', orient='records', indent=4)
            
        table = driver.find_element(By.XPATH, '//script[@id="community-table-data"]').get_attribute("innerText")
        table = json.loads(table)
        if table:
            table = pd.DataFrame(table)
            table = table.rename(columns={'method': 'Model'})
            title = driver.find_element(By.XPATH, '//div[@class="leaderboard-title"]/div/div/h1').text
            title = file_rename(title)
            table.to_json(f'{path_leaderboard}/pwc-community-{title}.json', orient='records', indent=4)
    
    driver.quit()