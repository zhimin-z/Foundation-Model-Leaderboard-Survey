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
    name = name.replace('-', '_')
    return name

folder = 'LawBench'
path_leaderboard = Path(f"data/{folder}")

column_names_extra = [
    "Dispute Focus Identification",
    "Marital Disputes Identification",
    "Issue Topic Identification",
    "Reading Comprehension",
    "Name Entity Recognition",
    "Opinion Summarization",
    "Argument Mining",
    "Event Detection",
    "Trigger Word Extraction",
    "Fact-based Article Prediction",
    "Scene-based Article Prediction",
    "Charge Prediction",
    "Prison Term Prediction w.o Article",
    "Prison Term Prediction w. Article",
    "Case Analysis",
    "Crimal Damages Calculation",
    "Consultation",
]

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://lawbench.opencompass.org.cn/leaderboard'
    driver.get(base_url)
    
    column_names = []
    for setting in driver.find_elements(By.XPATH, '//div[@class="ant-tabs-tab-btn"]'):
        setting.click()
        table = driver.find_element(By.XPATH, '//div[@class="ant-table-container"]')
        if not column_names:
            for column in table.find_elements(By.XPATH, ".//th[@scope='col']"):
                if column.text:
                    column_name = column.text
                elif column.get_attribute('aria-label'):
                    column_name = column.get_attribute('aria-label')
                else:
                    continue
                #     span_element = column.find_element(By.XPATH, './/span[@class="ant-table-column-title"]')
                #     column_name = span_element.text or span_element.find_element(By.XPATH, './span').text
                column_names.append(column_name)
            column_names.extend(column_names_extra)
        df = []
        for entry in table.find_elements(By.XPATH, './/tr[@class="ant-table-row ant-table-row-level-0"]'):
            entry_values = []
            for cell in entry.find_elements(By.XPATH, './/td')[1:]:
                entry_values.append(cell.text)
            df.append(pd.Series(entry_values, index=column_names))
        df = pd.DataFrame(df)
        df.to_json(path_leaderboard / f'shw-{name_process(setting.text)}.json', orient='records', indent=4)
                