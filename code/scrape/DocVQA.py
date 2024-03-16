import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/DocVQA"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://rrc.cvc.uab.es/?ch=17&com=evaluation&task=1'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table[@id="table-1-1"]')
    
    column_names = []
    for upper_column in table.find_elements(By.XPATH, './/thead/tr/th'):
        if upper_column.text:
            column_names.append(upper_column.text)
    
    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for value in row.find_elements(By.XPATH, './/td'):
            if value.text:
                values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Method': 'Model'}, inplace=True)
    df.to_json(f"{path_leaderboard}/ip.json", orient='records', indent=4)
