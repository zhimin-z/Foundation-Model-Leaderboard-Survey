import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/PubMedQA"


def prepcess_name(s):
    s = s.split('(')[-1][:-1]
    return s.lower()


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://pubmedqa.github.io'
    driver.get(url)
        
    table = driver.find_element(By.XPATH, '//table[@class="table table-responsive"]')
    column_names = ['Date']
    for column in table.find_elements(By.XPATH, './/thead/tr/th'):
        if column.text.strip():
            column_names.append(column.text)

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for name, value in zip(column_names, row.find_elements(By.XPATH, './/td')):
            if name == 'Date':
                values.append(value.text.split('\n')[-1])
            elif name == 'Code':
                try:
                    values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                except:
                    values.append('')
            else:
                values.append(value.text)
        df.append(values)
        
    df = pd.DataFrame(df, columns=column_names)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)