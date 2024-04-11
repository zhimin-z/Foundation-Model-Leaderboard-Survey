import pandas as pd
import time
import os
import re

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/WildBench"


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

    url = 'https://allenai-wildbench.hf.space'
    driver.get(url)
    
    table_indice = [0, -1]
    for button in driver.find_elements(By.XPATH, '//button[@id="od-benchmark-tab-table-ablation-button"]'):
        table_index = table_indice.pop(0)
        leaderboard_name = preprocess_name(button.text)
        button.click()
        input_box = driver.find_elements(By.XPATH, '//input[@data-testid="number-input"]')[table_index]
        
        for i in range(1, 11):
            input_box.clear()
            length_penalty = str(round(0.1*i, 1))
            input_box.send_keys(length_penalty)
            
            time.sleep(0.5)

            table = driver.find_elements(By.XPATH, '//table[@class="table svelte-1txh5yn"]')[table_index]
            column_names = [th.text for th in table.find_elements(By.XPATH, './/thead/tr/th')]
            
            df = []
            for row in table.find_elements(By.XPATH, './/tbody/tr'):
                values = [td.text for td in row.find_elements(By.XPATH, './/td')]
                df.append(values)
                
            df = pd.DataFrame(df, columns=column_names)
            df.drop(columns=['Rank'], inplace=True)
            df['Model'] = df['Model'].apply(lambda x: filter_string(x))
            df.to_json(f'{path_leaderboard}/hf-{leaderboard_name}-{length_penalty}.json', orient='records', indent=4)