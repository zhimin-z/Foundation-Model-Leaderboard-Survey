import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/OpenEval (text)"


def filter_first_row(s):
    parts = s.split("\n")
    return "\n".join(parts[1:]) if len(parts) > 1 else s


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    leaderboard_links = []
    base_url = 'http://openeval.org.cn/rank'
    driver.get(base_url)
    
    for option in driver.find_elements(By.XPATH, "//*[contains(@class, 'el-select-dropdown__item')]"):
        table_name = driver.execute_script("return arguments[0].innerText;", option)
        driver.execute_script("arguments[0].click();", option)
        
        column_names = ['Model']
        header = driver.find_element(By.XPATH, './/div[@class="el-table__header-wrapper"]')
        for column in header.find_elements(By.XPATH, './/div[@class="arrow"]'):
            column_name = driver.execute_script("return arguments[0].innerText;", column)
            column_names.append(column_name)
        
        df = []
        for row in driver.find_elements(By.XPATH, '//*[contains(@class, "el-table__row")]'):
            values = []
            for value in row.find_elements(By.XPATH, './/div[@class="cell"]'):
                values.append(value.text)
            df.append(values)
            
        df = pd.DataFrame(df, columns=column_names)
        df['Model'] = df['Model'].apply(filter_first_row)
        df.to_json(f'{path_leaderboard}/ip-{table_name}.json', orient='records', indent=4)
