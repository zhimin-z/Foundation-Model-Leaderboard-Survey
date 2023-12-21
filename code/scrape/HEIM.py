from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests

from pathlib import Path

path_llm = Path("data/llm")


def prepcess_name(s):
    s = s.lower()
    s = s.replace(":", "")
    s = s.replace(" ", "_")
    return s
    

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://crfm.stanford.edu/heim/latest/'
    driver.get(base_url)
    scenarios = driver.find_elements(By.XPATH, '//div[@class="col-sm-3"]')[1]
    scenario_url_lst = set()

    for scenario in scenarios.find_elements(By.XPATH, './/a'):
        scenario_url_lst.add(scenario.get_attribute('href'))

    scenario_url_lst = ['https://crfm.stanford.edu/heim/latest/?group=i2p']
    for scenario_url in scenario_url_lst:
        driver.get(scenario_url)
        table_names = driver.find_elements(By.XPATH, '//div[@class="table-container"]')
        tables = driver.find_elements(By.XPATH, '//table[@class="query-table results-table"]')
        for table_name, table in zip(table_names, tables):
            table_name = table_name.get_attribute('id')
            table_name = prepcess_name(table_name)
            column_names = []
            for column in table.find_elements(By.XPATH, './/thead/tr/td/span'):
                column_names.append(column.text)
            print(column_names)
        break
        # tasks = driver.find_elements(By.XPATH, '//a[text()="JSON"]')
        # for task in tasks[1:]:
        #     task_url = task.get_attribute('href').replace('benchmark_outputbenchmark_output', 'benchmark_output')
        #     response = requests.get(task_url)
        #     task_id = task_url.split('/')[-1].split('.')[0]
        #     with open(path_llm / f'HELM-leaderboard-{task_id}-20231024.json', 'wb') as file:
        #         file.write(response.content)
                