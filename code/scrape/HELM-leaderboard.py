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
    # posts = pd.DataFrame()
    # scenario_url_lst = {'https://crfm.stanford.edu/helm/latest/?group=cleva_closed_book_question_answering'}
    for scenario_url in scenario_url_lst:
        # print(scenario_url)
        driver.get(scenario_url)
        tasks = driver.find_elements(By.XPATH, '//a[text()="JSON"]')
        # tasks = driver.find_elements(By.XPATH, '//div[@class="col-sm-12"]')
        # print(len(tasks))
        # tasks = driver.find_elements(By.XPATH, '//div[@class="col-sm-12"]/div[2]/div/a')[:-1]
        # print(len(tasks))
        
# Execute JavaScript to get all attributes of the element
        # Check if element is located
    #     if tasks[0]:
    # # Execute JavaScript to get all attributes of the element
    #         all_attributes = driver.execute_script(
    #     """
    #     if (!arguments[0]) return null;
    #     var items = {}; 
    #     for (var index = 0; index < arguments[0].attributes.length; ++index) { 
    #         items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
    #     }; 
    #     return items;
    #     """, 
    #     tasks[0])

    # # Print all attributes if element is not None
    #         if all_attributes:
    #             print(all_attributes)
    #         else:
    #             print("Element has no attributes or is not defined.")
    #     else:
    #         print("Element not found.")

# Print all attributes
        # print(all_attributes)

        # tasks = driver.find_elements(By.XPATH, '//div[@class="col-sm-12"]/div[1]/a')
        # print(len(tasks))
        # print(tasks[0])
        
        # tasks = driver.find_elements(By.XPATH, '//div[@class="col-sm-12"]/div[1]/div/a')
        # print(len(tasks))
        for task in tasks[1:]:
            task_url = task.get_attribute('href').replace('benchmark_outputbenchmark_output', 'benchmark_output')
            # print()
            # task_id = task.get_attribute('href').split('=')[-1]
            # print(task_id)
            # task_url = json_url + task_id + '.json'
            # scenario_url = base_url + '?group=' + task
            response = requests.get(task_url)
            task_id = task_url.split('/')[-1].split('.')[0]
            with open(path_llm / f'HELM-leaderboard-{task_id}-20231024.json', 'wb') as file:
                file.write(response.content)
            # break
        # break
        # task = scenario_url.split('=')[-1]
        # scenario_url = base_url + '?group=' + task
        
        
        # scenario_url = json_url + task + '.json'
        # response = requests.get(scenario_url)
        
        
        # with open(path_llm / f'HELM-leaderboard-{task}-20231024.json', 'wb') as file:
        #     file.write(response.content)
