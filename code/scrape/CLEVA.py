from selenium.webdriver.common.by import By
from seleniumbase import Driver
import pandas as pd
import os

path_leaderboard = 'data/CLEVA'

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)
    
    url = 'http://www.lavicleva.com/#/homepage/table'
    driver.get(url)
    
    language_switcher = driver.find_element(By.XPATH, '//div[@class="container-content-top-right-e"]')
    driver.execute_script("arguments[0].click();", language_switcher)
    
    for table in driver.find_elements(By.XPATH, '//div[@class="home-content-graph-item"]'):
        header = table.find_element(By.XPATH, './/div[@class="el-table__header-wrapper"]')
        column_names = [driver.execute_script("return arguments[0].innerText;", column) for column in header.find_elements(By.XPATH, './/div[@class="cell"]')]

        body = table.find_element(By.XPATH, './/div[@class="el-table__body-wrapper is-scrolling-left"]')
        df = []
        for row in body.find_elements(By.XPATH, ".//*[contains(@class, 'el-table__row')]"):
            entry = []
            for value in row.find_elements(By.XPATH, './/div[@class="cell"]'):
                entry.append(driver.execute_script("return arguments[0].innerText;", value))
            df.append(entry)
            
        df = pd.DataFrame(df, columns=column_names)
        table_name = table.find_element(By.XPATH, './/div[@class="home-item-title"]').text
        df.to_json(f'{path_leaderboard}/ip-{table_name.lower()}.json', orient='records', indent=4)