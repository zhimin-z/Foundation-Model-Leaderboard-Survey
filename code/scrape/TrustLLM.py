import pandas as pd
import os
import re

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/TrustLLM"


def filter_string(text):
    regex_pattern = r'(↑)'
    filtered_string = re.sub(regex_pattern, '', text)
    return filtered_string.strip()

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://trustllmbenchmark.github.io/TrustLLM-Website/leaderboard.html'
    driver.get(url)
    
    leaderboard_names = [name.text.lower() for name in driver.find_elements(By.XPATH, '//div[@class="section"]/h2')]
    
    for leaderboard in driver.find_elements(By.XPATH, ".//table[contains(@id, 'table_')]"):
        column_names = [filter_string(column.text) for column in leaderboard.find_elements(By.XPATH, './/th')]
        
        df = []
        for row in leaderboard.find_elements(By.XPATH, './/tbody/tr'):
            values = [value.text for value in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'{path_leaderboard}/gh-{leaderboard_names.pop(0)}.json', orient='records', indent=4)
        