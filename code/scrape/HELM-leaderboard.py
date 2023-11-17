from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests

from pathlib import Path

path_llm = Path("data/llm")


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://crfm.stanford.edu/helm/latest/'
    driver.get(base_url)
    scenarios = driver.find_elements(By.XPATH, '//div[@class="col-sm-3"]')[1]
    scenario_url_lst = set()

    for scenario in scenarios.find_elements(By.XPATH, './/a'):
        scenario_url_lst.add(scenario.get_attribute('href'))

    json_url = 'https://storage.googleapis.com/crfm-helm-public/benchmark_output/releases/v0.3.0/groups/'
    for scenario_url in scenario_url_lst:
        driver.get(scenario_url)
        tasks = driver.find_elements(By.XPATH, '//a[text()="JSON"]')
        for task in tasks[1:]:
            task_url = task.get_attribute('href').replace('benchmark_outputbenchmark_output', 'benchmark_output')
            response = requests.get(task_url)
            task_id = task_url.split('/')[-1].split('.')[0]
            with open(path_llm / f'HELM-leaderboard-{task_id}-20231024.json', 'wb') as file:
                file.write(response.content)
                