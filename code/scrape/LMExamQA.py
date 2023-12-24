from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time
import re

path_leaderboard = "data/LMExamQA"
params = {
    "behavior": "allow",
    "downloadPath": path_leaderboard
}


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
    time.sleep(0.5)
    
    if name:
        table_name = name
    else:
        table_name = preprocess_name(table.text)

    df = []
    for row in driver.find_elements(By.XPATH, "//*[contains(@class, 'highcharts-series highcharts-series')]"):
        values = {
            'Model': row.get_attribute('aria-label').split(',')[0],
        }
        for cell in row.find_elements(By.XPATH, ".//*[contains(@class, 'highcharts-point')]"):
            value = cell.get_attribute('aria-label')
            column_name = value.split(',')[0]
            values[column_name] = extract_number(value)
        df.append(values)

    df = pd.DataFrame(df)
    df.to_json(f'{path_leaderboard}/shw-{table_name}.json',
               orient='records', indent=4)


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    base_url = 'https://lmexam.com'
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
