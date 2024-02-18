from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

def name_process(name, filter_keywords = []):
    name = name.lower()
    for keyword in filter_keywords:
        name = name.replace(keyword, '')
    name = name.split()
    name = '_'.join(name)
    name = name.replace('-', '_')
    return name

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://mmbench.opencompass.org.cn/leaderboard'
    driver.get(base_url)
    
    for index, benchmark_name in enumerate(driver.find_elements(By.XPATH, '//div[@class="ant-tabs-tab-btn"]')):
        path_leaderboard = "data/MMBench"
        benchmark_name.click()
        benchmark = driver.find_elements(By.XPATH, '//div[@class="_table_8bhzs_28"]')[index]
        table_names = benchmark.find_elements(By.XPATH, './/div[@class="_table-title_8bhzs_33"]')
        column_names = []
        tables = benchmark.find_elements(By.XPATH, './/div[@class="ant-table-container"]')
        for table_name, table in zip(table_names, tables):
            if not column_names:
                for column in table.find_elements(By.XPATH, ".//th"):
                    column_name = column.text if column.text else column.get_attribute('aria-label')
                    column_names.append(column_name)
            df = []
            for entry in table.find_elements(By.XPATH, './/tr[@class="ant-table-row ant-table-row-level-0"]'):
                entry_values = [entry.find_element(By.XPATH, './/div[@class="_model-name_xwhdx_1"]').text]
                for cell in entry.find_elements(By.XPATH, './/td[@class="ant-table-cell"]'):
                    entry_values.append(cell.text)
                df.append(pd.Series(entry_values, index=column_names))
            df = pd.DataFrame(df)
            df.rename(columns={'Method': 'Model'}, inplace=True)
            if 'ccbench' in benchmark_name.text.lower():
                path_leaderboard = "data/CCBench"
            if not os.path.exists(path_leaderboard):
                os.makedirs(path_leaderboard)
            df.to_json(f"{path_leaderboard}/iw-{name_process(benchmark_name.text, filter_keywords=['mmbench', 'ccbench'])}-{name_process(table_name.text)}.json", orient='records', indent=4)
                