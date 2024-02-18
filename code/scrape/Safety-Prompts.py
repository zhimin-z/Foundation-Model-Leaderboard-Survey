from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time
import os

path_leaderboard = "data/Safety-Prompts"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    base_url = 'http://115.182.62.166:18000'
    suffix_list = ['public', 'private']
    
    for suffix in suffix_list:
        url = f'{base_url}/{suffix}'
        driver.get(url)
        
        column_names = []
        for index, column in enumerate(driver.find_elements(By.XPATH, '//input[@class="el-checkbox__original"]')):
            if index < 1:
                continue
            column_names.append(column.get_attribute('value'))
            
        next_page = driver.find_element(By.XPATH, '//button[@class="btn-next"]')
            
        df = []
        while True:
            body1 = driver.find_element(By.XPATH, '//div[@class="el-table__fixed-body-wrapper"]')
            body2 = driver.find_element(By.XPATH, '//div[@class="el-table__body-wrapper is-scrolling-left"]')
            rows1 = body1.find_elements(By.XPATH, './/tr[@class="el-table__row"]')
            rows2 = body2.find_elements(By.XPATH, './/tr[@class="el-table__row"]')
            for row1, row2 in zip(rows1, rows2):
                entries = []
                for index, value in enumerate(row1.find_elements(By.XPATH, './/div[@class="cell"]')):
                    if (index > 0) and (index < 5):
                        entries.append(value.text)
                for index, value in enumerate(row2.find_elements(By.XPATH, './/div[@class="cell"]')):
                    if index < 5:
                        continue
                    elif index == 5:
                        link = value.find_element(By.XPATH, './/a[@class="href"]').get_attribute('href')
                        entries.append(link)
                    else:
                        entries.append(value.text)
                df.append(entries)
            if next_page.get_attribute('disabled') == 'true':
                break
            next_page.click()
            time.sleep(1)
            
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'{path_leaderboard}/iw-{suffix}.json', orient='records', indent=4)