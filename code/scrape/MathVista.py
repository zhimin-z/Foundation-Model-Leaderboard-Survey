import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/MathVista"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    url = 'https://mathvista.github.io'
    driver.get(url)

    leaderboard_names = []
    leaderboards = driver.find_elements(By.XPATH, '//section[@class="section"]')[2]
    for leaderboard_name in leaderboards.find_elements(By.XPATH, './/h2[@class="title is-3"]'):
        leaderboard_names.append(leaderboard_name.text.lower().replace('leaderboard on ', ''))
    
    for leaderboard_table in leaderboards.find_elements(By.XPATH, './/table[@class="js-sort-table"]'):
        column_names = []
        for column in leaderboard_table.find_elements(By.XPATH, './/thead/tr/td'):
            column_names.append(column.text)
        df = []
        for row in leaderboard_table.find_elements(By.XPATH, './/tbody/tr'):
            values = []
            for name, value in zip(column_names, row.find_elements(By.XPATH, './/td')):
                if name == 'Source':
                    values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                else:
                    values.append(value.text)
            df.append(values)
        df = pd.DataFrame(df, columns=column_names)
        df.drop(columns=['#'], inplace=True)
        df.to_json(f'{path_leaderboard}/gh-{leaderboard_names.pop(0)}.json', orient='records', indent=4)
