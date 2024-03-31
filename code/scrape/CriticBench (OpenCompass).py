import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/CriticBench (OpenCompass)"


def preprocess_text(s):
    s = s.lower()
    s = s.replace('leaderboard', '')
    s = s.strip()
    return s

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    for suffix in ['subjective', 'objective']:
        url = f'https://open-compass.github.io/CriticBench/leaderboard_{suffix}.html'
        driver.get(url)
        
        table = driver.find_element(By.XPATH, '//table[@id="origin"]')
        column_names = [column.text for column in table.find_elements(By.XPATH, '//thead/tr/th')]
        
        df = []
        for row in table.find_elements(By.XPATH, '//tbody/tr'):
            values = [value.text for value in row.find_elements(By.XPATH, './/td')]
            df.append(values)
            
        df = pd.DataFrame(df, columns=column_names)
        df.drop(columns=['#'], inplace=True)
        df.to_json(f'{path_leaderboard}/gh-{suffix}.json', orient='records', indent=4)

    driver.quit()