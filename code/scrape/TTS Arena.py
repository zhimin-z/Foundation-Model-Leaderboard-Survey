import pandas as pd
import time
import os
import re

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/TTS Arena"


def filter_string(text):
    regex_pattern = r'🔒|🔥'
    filtered_string = re.sub(regex_pattern, '', text)
    return filtered_string.strip()

    
def preprocess_name(s):
    s = s.lower()
    s = s.replace(' ', '_')
    return s


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    url = 'https://tts-agi-tts-arena.hf.space'
    driver.get(url)
    
    button = driver.find_element(By.XPATH, '//button[@id="component-37-button"]')
    button.click()
    time.sleep(0.5)
    
    column_names = [colunm.text for colunm in driver.find_elements(By.XPATH, '//tr[@slot="thead"]/th')]
    
    df = []
    for row in driver.find_elements(By.XPATH, '//tr[@slot="tbody"]'):
        values = [td.text for td in row.find_elements(By.XPATH, './/td')]
        df.append(values)
    
    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'name': 'Model'}, inplace=True)
    df.drop(columns=['order'], inplace=True)
    df.to_json(f'{path_leaderboard}/hf.json', orient='records', indent=4)
    
    driver.quit()