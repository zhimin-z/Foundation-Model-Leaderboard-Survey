from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time

path_leaderboard = "data/HELM"

def preprocess_name(s):
    s = s.lower().replace("/", "_").replace(" - ", "_").replace(": ", "_").replace(" ", "_")
    return s

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = f'https://crfm.stanford.edu/helm/classic/latest/#/leaderboard'
    driver.get(url)
        
        select = Select(driver.find_element(By.XPATH, '//select[@name="group" and @id="group"]'))
        for option in select.options:
            select.select_by_visible_text(option.text)
            group_name = preprocess_name(select.first_selected_option.text)
            time.sleep(1)
            
            scenarios = driver.find_elements(By.XPATH, '//div[@role="navigation"]/div')
            if scenarios:
                for index, scenario in enumerate(scenarios):
                    scenario.click()
                    time.sleep(0.5)
                    table_name = preprocess_name(scenario.text)
                    table = driver.find_element(By.XPATH, f'//table[@class="table w-full px-4"]')
                    column_names = [column.text for column in table.find_elements(By.XPATH, './/th/div/span')]
                    df = [[value.text for value in row.find_elements(By.XPATH, './/td')] for row in table.find_elements(By.XPATH, './/tbody/tr')]
                    df = pd.DataFrame(df, columns=column_names)
                    df.to_json(f'{path_leaderboard}/shw-{group_name}-{table_name}.json', orient='records', indent=4)
            else:
                table = driver.find_element(By.XPATH, f'//table[@class="table w-full px-4"]')
                column_names = [column.text for column in table.find_elements(By.XPATH, './/th/div/span')]
                df = [[value.text for value in row.find_elements(By.XPATH, './/td')] for row in table.find_elements(By.XPATH, './/tbody/tr')]
                df = pd.DataFrame(df, columns=column_names)
                df.to_json(f'{path_leaderboard}/shw-{group_name}.json', orient='records', indent=4)