from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json
import re
import os

def file_rename(title):
    title = title.lower()
    title = title.replace(',', '_').replace('/', '_').replace('-', '_').replace(':', '_').replace(' ', '_')
    return title

bloom = False
dataset = ''
path_leaderboard = 'data/The Pile'
included_leaderboards = ['language-modelling-on-the-pile']

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    leaderboard_links = []
    community_indicator = ''
    base_url = 'https://paperswithcode.com'
    
    if included_leaderboards:
        for match in included_leaderboards:
            link = f'{base_url}/sota/{match}'
            leaderboard_links.append(link)
    else:
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
