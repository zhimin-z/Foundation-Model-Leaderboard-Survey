from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import pickle
import time

def preprocess_name(s):
    s = s.lower().replace("/", "_").replace(" - ", "_").replace(": ", "_").replace(" ", "_")
    return s

def save(path_leaderboard, group_name, table_name):
    with open(f'{path_leaderboard}/checkpoint.pkl', 'wb') as file:
        checkpoint = {'group': group_name, 'scenario': table_name}
        pickle.dump(checkpoint, file)

def load(path_leaderboard):
    with open(f'{path_leaderboard}/checkpoint.pkl', 'rb') as file:
        return pickle.load(file)

if __name__ == '__main__':
    path_leaderboard = "data/HELM lite"
    
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = f'https://crfm.stanford.edu/helm/lite/latest/#/leaderboard'
    driver.get(url)
    
    select = Select(driver.find_element(By.XPATH, '//select[@name="group" and @id="group"]'))
    for option in select.options:
        select.select_by_visible_text(option.text)
        group_name = select.first_selected_option.text
        time.sleep(1)
        scenarios = driver.find_elements(By.XPATH, '//div[@role="navigation"]/div')
        if scenarios:
            for scenario in scenarios:
                scenario.click()
                time.sleep(0.5)
                table_name = scenario.text
                table = driver.find_element(By.XPATH, f'//table[@class="table w-full px-4"]')
                column_names = [column.text for column in table.find_elements(By.XPATH, './/th/div/span')]
                df = [[value.text for value in row.find_elements(By.XPATH, './/td')] for row in table.find_elements(By.XPATH, './/tbody/tr')]
                df = pd.DataFrame(df, columns=column_names)
                df.to_json(f'{path_leaderboard}/shw-{preprocess_name(group_name)}-{preprocess_name(table_name)}.json', orient='records', indent=4)
        else:
            table_name = ''
            table = driver.find_element(By.XPATH, f'//table[@class="table w-full px-4"]')
            column_names = [column.text for column in table.find_elements(By.XPATH, './/th/div/span')]
            df = [[value.text for value in row.find_elements(By.XPATH, './/td')] for row in table.find_elements(By.XPATH, './/tbody/tr')]
            df = pd.DataFrame(df, columns=column_names)
            df.to_json(f'{path_leaderboard}/shw-{preprocess_name(group_name)}.json', orient='records', indent=4)
        save(path_leaderboard, group_name, table_name)
