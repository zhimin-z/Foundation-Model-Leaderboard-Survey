from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json
import re
import os

def file_rename(title):
    title = title.lower()
    title = title.replace(',', '').replace('/', '').replace('-', '').replace(':', '')
    title = title.split()
    title = '_'.join(title)
    return title

bloom = False
dataset = ''
path_leaderboard = 'data/Common Voice'
included_leaderboards = ['speech-recognition-on-common-voice-8-0-17', 'automatic-speech-recognition-on-mozilla-109', 'speech-recognition-on-common-voice-8-0-5', 'automatic-speech-recognition-on-mozilla-103', 'speech-recognition-on-common-voice-8-0-13', 'speech-recognition-on-common-voice-9-0-french', 'speech-recognition-on-common-voice-7-0-27', 'speech-recognition-on-common-voice-8-0-15', 'speech-recognition-on-common-voice-8-0-32', 'speech-recognition-on-common-voice-8-0-33', 'automatic-speech-recognition-on-mozilla-73', 'automatic-speech-recognition-on-mozilla-79', 'speech-recognition-on-common-voice-8-0-21', 'speech-recognition-on-common-voice-8-0-35', 'automatic-speech-recognition-on-mozilla-82', 'speech-recognition-on-common-voice-7-0-19', 'speech-recognition-on-common-voice-7-0-3', 'automatic-speech-recognition-on-mozilla-91', 'speech-recognition-on-common-voice-8-0-14', 'speech-recognition-on-common-voice-7-0-irish', 'speech-recognition-on-common-voice-8-0-26', 'automatic-speech-recognition-on-mozilla-105', 'speech-recognition-on-common-voice-8-0-kyrgyz', 'speech-recognition-on-common-voice-8-0-irish', 'speech-recognition-on-common-voice-7-0-21', 'speech-recognition-on-common-voice-8-0-sakha', 'speech-recognition-on-common-voice-8-0-31', 'automatic-speech-recognition-on-mozilla-89', 'automatic-speech-recognition-on-mozilla-74', 'speech-recognition-on-common-voice-8-0-37', 'speech-recognition-on-common-voice-8-0-polish', 'speech-recognition-on-common-voice-8-0-18', 'speech-recognition-on-common-voice-7-0-13', 'speech-recognition-on-common-voice-8-0-6', 'speech-recognition-on-common-voice-7-0-8', 'speech-recognition-on-common-voice-7-0-4', 'speech-recognition-on-common-voice-8-0-tatar', 'speech-recognition-on-common-voice-8-0-16', 'speech-recognition-on-common-voice-8-0-breton', 'speech-recognition-on-common-voice-8-0-czech', 'speech-recognition-on-common-voice-8-0-4', 'speech-recognition-on-common-voice-8-0-22', 'speech-recognition-on-common-voice-8-0-german', 'speech-recognition-on-common-voice-welsh', 'automatic-speech-recognition-on-mozilla-84', 'speech-recognition-on-common-voice-8-0-basaa', 'speech-recognition-on-common-voice-8-0-french', 'speech-recognition-on-common-voice-chinese', 'automatic-speech-recognition-on-mozilla-72', 'automatic-speech-recognition-on-mozilla-75', 'speech-recognition-on-common-voice-frisian', 'speech-recognition-on-common-voice-italian', 'speech-recognition-on-common-voice-8-0-9', 'automatic-speech-recognition-on-mozilla-88', 'speech-recognition-on-common-voice-8-0', 'speech-recognition-on-common-voice-8-0-19', 'automatic-speech-recognition-on-mozilla-77', 'speech-recognition-on-common-voice-8-0-hindi', 'speech-recognition-on-common-voice-8-0-20', 'automatic-speech-recognition-on-mozilla-65', 'automatic-speech-recognition-on-mozilla-71', 'speech-recognition-on-common-voice-7-0-29', 'automatic-speech-recognition-on-mozilla-67', 'automatic-speech-recognition-on-common-voice-15', 'speech-recognition-on-common-voice-7-0-hindi', 'speech-recognition-on-common-voice-8-0-dutch', 'speech-recognition-on-common-voice-7-0-5', 'speech-recognition-on-common-voice-french', 'speech-recognition-on-common-voice-spanish', 'speech-recognition-on-common-voice-german', 'automatic-speech-recognition-on-mozilla-66']

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
