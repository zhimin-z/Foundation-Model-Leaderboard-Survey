import pandas as pd
import time
import re
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Chatbot Arena Leaderboard"
leaderboard_names = ['arena_leaderboard', 'full_leaderboard']

def filter_string(text):
    regex_pattern = r'🤖|⭐|📈|📚|📊|🗳️'
    filtered_string = re.sub(regex_pattern, '', text)
    return filtered_string.strip()


def prepcess_name(s):
    s = s.lower()
    s = s.replace(' ', '_')
    return s


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://chat.lmsys.org'
    driver.get(url)
    time.sleep(10)

    leaderboard_button = driver.find_element(By.XPATH, '//button[@aria-controls="component-140"]')
    leaderboard_button.click()
    
    for leaderboard_name in leaderboard_names:
        leaderboard = driver.find_element(By.XPATH, f'//table[@class="table svelte-1jok1de"]')
        column_names = []
        for column in leaderboard.find_elements(By.XPATH, './/thead/tr/th'):
            column_name = filter_string(column.text)
            column_names.append(column_name)
        
        df = set()
        while True:
            # Find the current set of rows
            current_df = set()
            for row in leaderboard.find_elements(By.XPATH, './/tbody/tr'):
                values = tuple(value.text for value in row.find_elements(By.XPATH, './/td'))
                df.add(values)
        
            # Attempt to scroll
            driver.execute_script("arguments[0].scrollTop += 200;", leaderboard)
            time.sleep(0.5)  # Adjust based on the loading time, ensuring that new rows load
            
            if current_df.issubset(df):
                # No new rows found, assuming all rows are loaded
                break
            else:
                df.update(current_df)
        
        df = [list(tup) for tup in df]
        df = pd.DataFrame(df, columns=column_names)
        
        if 'Rank' in df.columns:
            df = df.drop('Rank', axis=1)
        df.to_json(f'{path_leaderboard}/iw-{leaderboard_name}.json',
                   orient='records', indent=4)
        
    driver.quit()