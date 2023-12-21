from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/HELM"

def prepcess_name(s):
    s = s.lower()
    s = s.replace(" - ", "_")
    s = s.replace(": ", "_")
    s = s.replace(" ", "_")
    return s


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    versions = ['classic', 'lite']
    for version in versions:
        url = f'https://crfm.stanford.edu/helm/{version}/latest/#/leaderboard'
        driver.get(url)
        
        for index in range(len(Select(driver.find_element(By.XPATH, '//select[@id="group"]')).options)):
            select = Select(driver.find_element(By.XPATH, '//select[@id="group"]'))
            select.select_by_index(index)
            group_name = prepcess_name(select.first_selected_option.text)
            
            for scenario in driver.find_elements(By.XPATH, '//div[@role="navigation"]/div'):
                scenario.click()
                table_name = prepcess_name(scenario.text)
                
                table = driver.find_element(By.XPATH, f'//table[@class="table w-full px-4"]')
                column_names = [column.text for column in table.find_elements(By.XPATH, './/span')]
                
                df = []
                for row in table.find_elements(By.XPATH, './/tbody/tr'):
                    series = {}
                    values = row.find_elements(By.XPATH, './/td')
                    for column_name, value in zip(column_names, values):
                        series[column_name] = value.text
                    df.append(series)
                 
                df = pd.DataFrame(df)
                if table_name:
                    file_name = f'{path_leaderboard}/shw-{version}-{group_name}-{table_name}.json'
                else:
                    file_name = f'{path_leaderboard}/shw-{version}-{group_name}.json'
                df.to_json(file_name, orient='records', indent=4)