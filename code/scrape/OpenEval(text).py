from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json
import re

from pathlib import Path

def file_rename(folder, title):
    title = title.lower().replace(f' on {folder.lower()}', '')
    title = title.replace(' / ', '_').replace(' - ', '_').replace('-', '_').replace(' ', '_')
    return title

folder = 'OpenEval(text)'
path_leaderboard = Path(f"data/{folder}")

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    leaderboard_links = []
    base_url = 'http://openeval.org.cn/rank'
    driver.get(base_url)
    
    for option in driver.find_elements(By.XPATH, '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li'):
        table_name = option.text
        print(table_name)
        option.click()
        for column in driver.find_elements(By.XPATH, '//table[@class="el-table__header"]/thead/tr/th'):
            print(f'{table_name}, {column.text}')
    
    
    
# table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
# table.to_json(path_leaderboard / f'pwc-{title}.json', orient='records', indent=4)
