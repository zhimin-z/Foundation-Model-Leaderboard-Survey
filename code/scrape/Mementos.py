import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Mementos"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    url = 'https://mementos-bench.github.io'
    driver.get(url)

    df = []
    table = driver.find_elements(By.XPATH, '//table[@class="js-sort-table"]/tbody/tr')
    for index, row in enumerate(table):
        if index:
            values = []
            for column in row.find_elements(By.XPATH, './/td'):
                if column.text == 'Link':
                    values.append(column.find_element(By.XPATH, './/a').get_attribute('href'))
                else:
                    values.append(column.text)
            df.append(values)
        else:
            column_names = [column.text for column in row.find_elements(By.XPATH, './/td')]
            
    df = pd.DataFrame(df, columns=column_names)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
