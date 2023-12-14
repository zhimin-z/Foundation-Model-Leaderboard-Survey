from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

from pathlib import Path

def name_process(name, filter_keywords = []):
    name = name.lower()
    for keyword in filter_keywords:
        name = name.replace(keyword.lower(), '')
    name = name.split()
    name = '_'.join(name)
    return name

folder = 'Large Language Model Leaderboard'
path_leaderboard = Path(f"data/{folder}")

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://opencompass.org.cn/leaderboard-llm'
    driver.get(base_url)
    
    for benchmark in driver.find_elements(By.CSS_SELECTOR, '[class*="_inline-tab-item_vl7j5_8"]'):
        benchmark.click()
        capabilities = driver.find_elements(By.XPATH, f'//div[@class="ant-tabs-tab-btn"]')
        for index, capability in enumerate(capabilities):
            capability.click()
            table = driver.find_elements(By.XPATH, '//div[@class="ant-table-container"]')[index]
            column_names = []
            for column in table.find_elements(By.XPATH, ".//th"):
                if column.text:
                    column_name = column.text
                elif column.get_attribute('aria-label'):
                    column_name = column.get_attribute('aria-label')
                else:
                    column_name = column.find_element(By.XPATH, './/a').get_attribute('href').split('/')[-1]
                column_names.append(column_name)
            df = []
            for entry in table.find_elements(By.XPATH, './/tr[@class="ant-table-row ant-table-row-level-0"]'):
                entry_values = []
                for cell in entry.find_elements(By.XPATH, './/td')[1:]:
                    entry_values.append(cell.text)
                df.append(pd.Series(entry_values, index=column_names))
            df = pd.DataFrame(df)
            df.to_json(path_leaderboard / f'shw-{name_process(benchmark.text)}-{name_process(capability.text)}.json', orient='records', indent=4)