import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/OpenCompass LLM Leaderboard (v2)"
url = 'https://rank.opencompass.org.cn/leaderboard-llm-v2'


def preprocess_name(name):
    name = name.lower()
    name = name.replace(' benchmarks', '')
    name = name.replace(' ', '_')
    return name


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)
    driver.get(url)
    
    for benchmark in driver.find_elements(By.XPATH, '//div[@class="_inline-tab_vl7j5_1"]/div'):
        benchmark.click()
        benchmark_category = preprocess_name(benchmark.text)
        index = 1
        while True:
            try:
                button = driver.find_element(By.XPATH, f'//div[@data-node-key="tab{index}"]/div')
                capability_category = preprocess_name(button.text)
                button.click()
        
                column_names = []
                head = driver.find_elements(By.XPATH, f'//thead[@class="ant-table-thead"]')[index-1]
                for column in head.find_elements(By.XPATH, f'.//tr/th'):
                    if column.text.strip():
                        column_names.append(column.text)
                    else:
                        column_names.append(column.get_attribute('aria-label'))
            
                df = []
                body = driver.find_elements(By.XPATH, f'//tbody[@class="ant-table-tbody"]')[index-1]
                for row in body.find_elements(By.XPATH, f'.//tr')[1:]:
                    values = [column.text for column in row.find_elements(By.XPATH, './/td')[1:]]
                    df.append(values)
            
                df = pd.DataFrame(df, columns=column_names)
                df.to_json(f'{path_leaderboard}/ip-{benchmark_category}-{capability_category}.json', orient='records', indent=4)
            
                index += 1
            except:
                break
