import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/MathVerse"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://mathverse-cuhk.github.io'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table[@class="js-sort-table"]')
        

    column_names = []
    upper_columns, lower_columns = table.find_elements(By.XPATH, '//thead/tr')
    lower_column_list = [lower_column.text for lower_column in lower_columns.find_elements(By.XPATH, './/th')]
    for upper_column in upper_columns.find_elements(By.XPATH, './/th'):
        try:
            for _ in range(int(upper_column.get_attribute('colspan'))):
                column_names.append(f'{upper_column.text} ({lower_column_list.pop(0)})')
        except:
            column_names.append(upper_column.text)
        

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for name, value in zip(column_names, row.find_elements(By.XPATH, './/td')):
            if name == 'Source':
                values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
            else:
                values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=['#'], inplace=True)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
    
    driver.quit()