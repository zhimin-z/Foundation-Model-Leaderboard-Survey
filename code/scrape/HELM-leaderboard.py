from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
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
    posts = pd.DataFrame()
    
    for post_url in scenario_url_lst:
        task = post_url.split('=')[-1]
        post_url = json_url + task + '.json'
        response = requests.get(post_url)
        with open(path_llm / f'HELM-leaderboard-{task}-20231024.json', 'wb') as file:
            file.write(response.content)
