from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/HELM"
# substrings_to_remove = [" \u2191", " \u2193"]


# def remove_substrings(s, substrings=substrings_to_remove):
#     for substring in substrings:
#         s = s.replace(substring, '')
#     return s


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
            
            for table in driver.find_elements(By.XPATH, '//div[@role="navigation"]/div'):
                table.click()
                table_name = prepcess_name(table.text)
                
                column_names = [column.text for column in table.find_elements(By.XPATH, './/span')]
                
                df = []
                content = driver.find_element(By.XPATH, '//table[@class="table w-full px-4"]')
                for row in content.find_elements(By.XPATH, './/tbody/tr'):
                    series = {}
                    values = row.find_elements(By.XPATH, './/td')
                    for column_name, value in zip(column_names, values):
                        series[column_name] = value.text
                    df.append(series)
                    
                df = pd.DataFrame(df)
                df.to_json(f'{path_leaderboard}/shw-{group_name}-{table_name}.json', orient='records', indent=4)
            break
        break

    # for scenario in scenarios.find_elements(By.XPATH, './/a'):
    #     scenario_url_lst.add(scenario.get_attribute('href'))
        
    # for scenario_url in scenario_url_lst:
    #     driver.get(scenario_url)
    #     print(scenario_url)
        
    #     table_names = driver.find_elements(By.XPATH, '//div[@class="table-container"]')
    #     if len(table_names) < 2:
    #         table_names = [driver.find_element(By.XPATH, '//div[@class="col-sm-12"]/div/h3').text]
    #     else:
    #         table_names = [table_name.get_attribute('id') for table_name in table_names]
            
    #     tables = driver.find_elements(By.XPATH, '//table[@class="query-table results-table"]')
    #     for table_name, table in zip(table_names, tables):
    #         column_names = [remove_substrings(column.text) for column in table.find_elements(By.XPATH, './/thead/tr/td/span')]
            
    #         df = []
    #         for row in table.find_elements(By.XPATH, './/tbody/tr'):
    #             series = {}
    #             values = row.find_elements(By.XPATH, './/span')
    #             for column_name, value in zip(column_names, values):
    #                 series[column_name] = value.text
    #             df.append(series)

    #         df = pd.DataFrame(df)
    #         df.to_json(f'{path_leaderboard}/shw-{prepcess_name(table_name)}.json', orient='records', indent=4)