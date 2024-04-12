import pandas as pd
import os
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = 'data/LMSYS Chatbot Arena Leaderboard'
options = ['Overall', 'Coding', 'Longer Query', 'English', 'Chinese', 'French', 'Exclude Ties', 'Exclude Short']


def preprocess_text(s):
    s = s.lower()
    s = s.replace('leaderboard', '')
    s = s.strip()
    s = s.replace(' ', '_')
    return s

def filter_string(text):
    regex_pattern = r'🤖|⭐|📚|📈|📊|🗳️'
    filtered_string = re.sub(regex_pattern, '', text)
    return filtered_string.strip()

def save_table(driver, index, leaderboard_name):
    table = driver.find_elements(By.XPATH, '//table[@class="table svelte-1jok1de"]')[index]
    column_names = [filter_string(column.text) for column in table.find_elements(By.XPATH, './/th')]
    print(column_names)
            
    df = []
    for row in table.find_elements(By.XPATH, './/tr'):
        values = [value.text for value in row.find_elements(By.XPATH, './/td')]
        df.append(values)
            
    df = pd.DataFrame(df, columns=column_names)
    df.dropna(subset=['Model'], inplace=True)
    if 'Rank' in column_names:
        df.drop(columns=['Rank', 'Delta'], inplace=True)
    df.to_json(f'{path_leaderboard}/hf-{leaderboard_name}.json', orient='records', indent=4)

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    url = 'https://lmsys-chatbot-arena-leaderboard.hf.space'
    driver.get(url)
    
    for index, button in enumerate(driver.find_elements(By.XPATH, '//button[contains(@class, "svelte-kqij2n")]')):
        leaderboard_name = preprocess_text(button.text)
        button.click()
        
        if index:
            save_table(driver, index, leaderboard_name)
        else:
            inputbox = driver.find_element(By.XPATH, '//input[@class="border-none svelte-tq78c3"]')
            for option in options:
                inputbox.clear()
                inputbox.send_keys(option)
                inputbox.send_keys(Keys.ENTER)
                leaderboard_name_with_option = f'{leaderboard_name}-{preprocess_text(option)}'
                save_table(driver, index, leaderboard_name_with_option)

    driver.quit()
