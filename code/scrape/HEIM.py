import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/HEIM"
substrings_to_remove = [" \u2191", " \u2193"]


def remove_substrings(s, substrings=substrings_to_remove):
    for substring in substrings:
        s = s.replace(substring, '')
    return s


def prepcess_name(s):
    s = s.lower()
    s = s.replace(" - ", "_")
    s = s.replace(": ", "_")
    s = s.replace(" ", "_")
    return s


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    base_url = 'https://crfm.stanford.edu/heim/latest'
    driver.get(base_url)
    
    scenarios = driver.find_elements(By.XPATH, '//div[@class="col-sm-3"]')[1]
    scenario_url_lst = set()

    for scenario in scenarios.find_elements(By.XPATH, './/a'):
        scenario_url_lst.add(scenario.get_attribute('href'))
        
    for scenario_url in scenario_url_lst:
        driver.get(scenario_url)
        print(scenario_url)
        
        table_names = driver.find_elements(By.XPATH, '//div[@class="table-container"]')
        if len(table_names) < 2:
            table_names = [driver.find_element(By.XPATH, '//div[@class="col-sm-12"]/div/h3').text]
        else:
            table_names = [table_name.get_attribute('id') for table_name in table_names]
            
        tables = driver.find_elements(By.XPATH, '//table[@class="query-table results-table"]')
        for table_name, table in zip(table_names, tables):
            column_names = [remove_substrings(column.text) for column in table.find_elements(By.XPATH, './/thead/tr/td/span')]
            
            df = []
            for row in table.find_elements(By.XPATH, './/tbody/tr'):
                series = {}
                values = row.find_elements(By.XPATH, './/span')
                for column_name, value in zip(column_names, values):
                    series[column_name] = value.text
                df.append(series)

            df = pd.DataFrame(df)
            df.to_json(f'{path_leaderboard}/ip-{prepcess_name(table_name)}.json', orient='records', indent=4)