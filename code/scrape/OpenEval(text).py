from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import re

from pathlib import Path

folder = 'OpenEval(text)'
path_leaderboard = Path(f"data/{folder}")

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    leaderboard_links = []
    base_url = 'http://openeval.org.cn/rank'
    driver.get(base_url)
    
    wait = WebDriverWait(driver, 10)
    
    for option in driver.find_elements(By.XPATH, "//*[contains(@class, 'el-select-dropdown__item')]"):
        table_name = option.find_element(By.XPATH, ".//span").text
        driver.execute_script("arguments[0].click();", option)
        header = driver.find_element(By.XPATH, './/table[@class="el-table__header"]')
        column_names = []
        for column in header.find_elements(By.XPATH, './/div[@class="cell"]'):
            # element = wait.until(EC.presence_of_element_located((By.XPATH, ".//span")))
            column_names.append(column.find_element(By.XPATH, './/span').text)
            # column_names.append(element.text)
        print(table_name)
        print(column_names)
    
# table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
# table.to_json(path_leaderboard / f'pwc-{title}.json', orient='records', indent=4)
