import pandas as pd
import time
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
            
def extract_data_to_dataframe(scrollable, df):
    for row in scrollable.find_elements(By.XPATH, './/tbody/tr'):
        values = [value.text for value in row.find_elements(By.XPATH, './/td')]
        df.loc[len(df)] = values
        
def save_table(driver, index, leaderboard_name):
    scrollable = driver.find_elements(By.XPATH, '//table[@class="table svelte-1jok1de"]')[index]
    driver.execute_script("arguments[0].scrollTop = 0", scrollable)
    
    column_names = [filter_string(column.text) for column in scrollable.find_elements(By.XPATH, './/thead/tr/th')]

    df = pd.DataFrame(columns=column_names)
    extract_data_to_dataframe(scrollable, df)
    
    increment = 500
    while True:
        # Scroll down to the bottom of the table element
        driver.execute_script("arguments[0].scrollTop += arguments[1]", scrollable, increment)
        
        # Wait for the table to load new rows
        time.sleep(0.5)
        extract_data_to_dataframe(scrollable, df)

        # Check if the scroll has reached the bottom of the table
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable)
        if int(scrollable.get_attribute('scrollTop')) + scrollable.size['height'] >= new_height:
            break

    df.drop_duplicates(inplace=True)
    if 'Rank' in column_names:
        df.drop(columns=['Rank'], inplace=True)
    if 'Delta' in column_names:
        df.drop(columns=['Delta'], inplace=True)
    df.to_json(f'{path_leaderboard}/ip-{leaderboard_name}.json', orient='records', indent=4)

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
                time.sleep(5)
                
                leaderboard_name_with_option = f'{leaderboard_name}-{preprocess_text(option)}'
                save_table(driver, index, leaderboard_name_with_option)

    driver.quit()
