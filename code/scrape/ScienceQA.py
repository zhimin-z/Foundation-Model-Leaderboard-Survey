import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/ScienceQA"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://scienceqa.github.io/leaderboard.html'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table[@class="js-sort-table"]')
    column_names = []
    for column in table.find_elements(By.XPATH, './/thead/tr/td'):
        column_names.append(column.text)

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for name, value in zip(column_names, row.find_elements(By.XPATH, './/td')):
            if name == 'Link':
                values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
            else:
                values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=['#'], inplace=True)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
    