import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/OpenCompass Large Language Model Leaderboard"
url = 'https://rank.opencompass.org.cn/leaderboard-llm'


def preprocess_name(name):
    name = name.lower()
    name = name.replace(' benchmarks', '')
    return name


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(10)
    driver.get(url)
    
    for benchmark in driver.find_elements(By.XPATH, '//div[contains(@class, "_inline-tab-item_vl7j5_8")]'):
        driver.execute_script("arguments[0].click();", benchmark)
        benchmark_name = preprocess_name(benchmark.text)
        
        for index, leaderboard in enumerate(driver.find_elements(By.XPATH, '//div[@class="ant-tabs-nav-list"]/div')[:-1]):
            leaderboard_name = leaderboard.get_attribute('data-node-key')
            driver.execute_script("arguments[0].click();", leaderboard)
            
            column_names = []
            head = driver.find_elements(By.XPATH, f'//thead[@class="ant-table-thead"]')[index]
            for column in head.find_elements(By.XPATH, f'.//tr/th'):
                if column.text.strip():
                    column_names.append(column.text)
                else:
                    column_names.append(column.get_attribute('aria-label'))
            
            df = []
            body = driver.find_elements(By.XPATH, f'//tbody[@class="ant-table-tbody"]')[index]
            for row in body.find_elements(By.XPATH, f'.//tr')[1:]:
                values = [column.text for column in row.find_elements(By.XPATH, './/td')]
                df.append(values)
            
            df = pd.DataFrame(df, columns=column_names)
            df.drop(columns=[None], inplace=True)
            df.to_json(f'{path_leaderboard}/ip-{benchmark_name}-{leaderboard_name}.json', orient='records', indent=4)

driver.quit()