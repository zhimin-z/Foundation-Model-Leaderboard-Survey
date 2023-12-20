from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

from pathlib import Path

folder = 'OpenEval(text)'
path_leaderboard = Path(f"data/{folder}")

if __name__ == '__main__':
    driver = uc.Chrome()
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
        df.to_json(path_leaderboard / f'shw-{table_name}.json', orient='records', indent=4)
