from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import re
import os
import time

path_leaderboard = "data/LMExamQA"

def get_latest_file(dir_path):
    files = os.listdir(dir_path)
    paths = [os.path.join(dir_path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def download(driver, table):
    table.click()
    menu = driver.find_element(By.XPATH, '//button[@class="highcharts-a11y-proxy-element highcharts-no-tooltip"]')
    menu.click()
    download = driver.find_elements(By.XPATH, '//li[@class="highcharts-menu-item"]')[6]
    download.click()
    time.sleep(5)
    latest_file = get_latest_file(path_leaderboard)
    os.rename(latest_file, f'{path_leaderboard}/shw-{preprocess_name(table.text)}.csv')

def preprocess_name(s):
    s = s.lower()
    s = s.split()[:-1]
    s = ' '.join(s)
    return s

def extract_number(s):
    match = re.search(r'-?\b\d+(?:\.\d+)?\b', s)
    return match.group(0) if match else None

def retrieve_table(driver, table, name=''):
    table.click()
    # print(table.text)
    if name:
        table_name = name
    else:
        table_name = preprocess_name(table.text)
    # print(table_name)
    # time.sleep(1)
    
    df = []
    # table = driver.find_element(By.XPATH, '//g[@class="highcharts-series-group"]')
    for row in driver.find_elements(By.XPATH, "//*[contains(@class, 'highcharts-series highcharts-series')]"):
        # print(row.tag_name)
        values = {
            'Model': row.get_attribute('aria-label').split(',')[0],
        }
        for cell in row.find_elements(By.XPATH, ".//*[contains(@class, 'highcharts-point')]"):
            value = cell.get_attribute('aria-label')
            column_name = value.split(',')[0]
            values[column_name] = extract_number(value)
        df.append(values)
        # print(values)

    df = pd.DataFrame(df)
    df.to_json(f'{path_leaderboard}/shw-{table_name}.json', orient='records', indent=4)
    time.sleep(1)

if __name__ == '__main__':
    driver = uc.Chrome()

    params = {
        "behavior": "allow",
        "downloadPath": path_leaderboard
    }
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    driver.implicitly_wait(5)

    base_url = 'https://lmexam.com/'

    # driver.execute_cdp_cmd(
    #     "Browser.grantPermissions",
    #     {
    #         "origin": base_url,
    #         "permissions": ["geolocation"]
    #     },
    # )

    driver.get(base_url)

    zero = driver.find_element(By.XPATH, '//button[@id="pills-result-tab"]')
    retrieve_table(driver, zero, name='overall')

    for first in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-primary"]'):
        retrieve_table(driver, first)
        for second in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-danger"]'):
            retrieve_table(driver, second)
            for third in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-warning"]'):
                retrieve_table(driver, third)
                for fourth in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-success"]'):
                    retrieve_table(driver, fourth)
                    for fifth in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-info"]'):
                        retrieve_table(driver, fifth)
