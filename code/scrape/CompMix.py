import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/CompMix"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://qa.mpi-inf.mpg.de/compmix'
    driver.get(url)
        
    for table in driver.find_elements(By.XPATH, '//table[@class="table"]'):
        column_names = []
        for column in table.find_elements(By.XPATH, './/thead/tr/th'):
            column_names.append(column.text)

        df = []
        for row in table.find_elements(By.XPATH, './/tbody/tr'):
            values = [value.text for value in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'{path_leaderboard}/iw.json', orient='records', indent=4)