from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = 'http://www.lavicleva.com/#/homepage/table'
    driver.get(url)
    time.sleep(1)
    
    language_switcher = driver.find_element(By.XPATH, '//div[@class="container-content-top-right-e"]')
    driver.execute_script("arguments[0].click();", language_switcher)
    
    for table in driver.find_elements(By.XPATH, '//div[@class="home-content-graph-item"]'):
        name = table.find_element(By.XPATH, './/div[@class="home-item-title"]').text
        header = table.find_element(By.XPATH, './/div[@class="el-table__header-wrapper"]')
        column_names = [column.text for column in header.find_elements(By.XPATH, './/div[@class="cell"]')]
        print(column_names)
        body = table.find_element(By.XPATH, './/div[@class="el-table__body-wrapper is-scrolling-left"]')
        df = []
        for row in body.find_elements(By.XPATH, "//*[contains(@class, 'el-table__row')]"):
            entry = []
            for value in row.find_elements(By.XPATH, './/div[@class="cell"]'):
                entry.append(value.text)
            df.append(entry)
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'data/CLEVA/shw-{name}.json', orient='records', indent=4)