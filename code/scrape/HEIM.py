from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/HEIM"
substrings_to_remove = [" \u2191", " \u2193"]


def remove_substrings(s, substrings=substrings_to_remove):
    for substring in substrings:
        s = s.replace(substring, '')
    return s


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
        
    for scenario_url in scenario_url_lst:
        driver.get(scenario_url)
        table_names = driver.find_elements(
            By.XPATH, '//div[@class="table-container"]')
        tables = driver.find_elements(
            By.XPATH, '//table[@class="query-table results-table"]')

        for table_name, table in zip(table_names, tables):
            table_name = table_name.get_attribute('id')
            table_name = prepcess_name(table_name)

            column_names = []
            for column in table.find_elements(By.XPATH, './/thead/tr/td/span'):
                column_name = remove_substrings(column.text)
                column_names.append(column_name)

            df = []
            for row in table.find_elements(By.XPATH, './/tbody/tr'):
                values = []
                for value in row.find_elements(By.XPATH, './/span'):
                    values.append(value.text)
                df.append(values)

            df = pd.DataFrame(df, columns=column_names)
            df.to_json(f'{path_leaderboard}/shw-{table_name}.json',
                       orient='records', indent=4)