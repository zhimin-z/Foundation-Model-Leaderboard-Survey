import pandas as pd
import time
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/SuperBench"
url = 'https://fm.ai.tsinghua.edu.cn/superbench/#/leaderboard'

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)
    driver.get(url)
    
    for option in driver.find_elements(By.XPATH, '//div[@class="nav"]/div'):
        leaderboard_name = option.text
        option.click()
        time.sleep(5)
        
        column_names = []
        try:
            upper_columns, lower_columns = driver.find_elements(By.XPATH, '//table[@class="el-table__header"]/thead/tr')
            lower_column_list = [lower_column.text for lower_column in lower_columns.find_elements(By.XPATH, './/th')]
            for upper_column in upper_columns.find_elements(By.XPATH, './/th'):
                colspan = int(upper_column.get_attribute('colspan'))
                if colspan > 1:
                    for _ in range(colspan):
                        column_names.append(f'{upper_column.text} ({lower_column_list.pop(0)})')
                else:
                    column_names.append(upper_column.text)
        except:
            for upper_column in driver.find_elements(By.XPATH, '//table[@class="el-table__header"]/thead/tr/th'):
                if upper_column.text:
                    column_names.append(upper_column.text)
        
        df = []
        for row in driver.find_elements(By.XPATH, '//tr[@class="el-table__row"]'):
            values = [value.text for value in row.find_elements(By.XPATH, './/td')]
            df.append(values)
            
        df = pd.DataFrame(df, columns=column_names)
        df.rename(columns={'模型': 'Model'}, inplace=True)
        df.to_json(f'{path_leaderboard}/ip-{leaderboard_name}.json', orient='records', indent=4)
        
    driver.quit()