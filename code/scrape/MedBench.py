from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time
import os

path_leaderboard = "data/MedBench"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://medbench.opencompass.org.cn/leaderboard'
    driver.get(url)
    time.sleep(5)
    
    for index, page in enumerate(driver.find_elements(By.XPATH, '//div[@class="ant-tabs-nav-list"]/div')[:-1]):
        page.click()
        leaderboard = driver.find_elements(By.XPATH, '//div[@class="ant-table-container"]')[index]
        
        column_names = []
        for column in leaderboard.find_elements(By.XPATH, './/thead[@class="ant-table-thead"]/tr/th'):
            column_name = driver.execute_script("return arguments[0].innerText;", column).strip()
            column_names.append(column_name)
        
        df = []
        for row in leaderboard.find_elements(By.XPATH, './/tbody[@class="ant-table-tbody"]/tr')[1:]:
            values = []
            for value in row.find_elements(By.XPATH, './/td')[1:]:
                values.append(value.text)
            df.append(values)
        
        df = pd.DataFrame(df, columns=column_names)
        df.rename(columns={'模型名称': 'Model'}, inplace=True)
        df.to_json(f'{path_leaderboard}/iw-{page.text}.json', orient='records', indent=4)