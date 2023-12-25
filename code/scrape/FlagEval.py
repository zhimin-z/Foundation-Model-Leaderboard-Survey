from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time

path_leaderboard = "data/FlagEval"

def prepcess_name(s):
    s = s.lower()
    s = s.replace(" - ", "_")
    s = s.replace(": ", "_")
    s = s.replace(" ", "_")
    return s

def concatenate_elements(*expanded_lists):
    # Ensure all lists are of the same length
    length_of_lists = len(expanded_lists[0])
    if not all(len(lst) == length_of_lists for lst in expanded_lists):
        raise ValueError("All lists must be of the same length.")

    # Extract the first element of each tuple in each list
    extracted_elements = [[elem[0] for elem in lst] for lst in expanded_lists]

    # Concatenate elements with the same index, ignoring empty strings
    concatenated_results = []
    for i in range(length_of_lists):
        elements = [extracted_elements[j][i] for j in range(len(expanded_lists)) if extracted_elements[j][i]]
        concatenated_results.append("\n".join(elements))

    return concatenated_results

def retrieve_table(driver):
    column_list = driver.find_elements(By.XPATH, '//thead[@class="is-group"]/tr')
    match len(column_list):
        case 3:
            upper_columns_mapping = []
            middle_columns_mapping = []
            lower_columns_mapping = []
            upper_columns, middle_columns, lower_columns = column_list
            for column in upper_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                upper_columns_mapping.append(value)
            for column in middle_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                middle_columns_mapping.append(value)
            for column in lower_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                lower_columns_mapping.append(value)
            for index, (_, rowspan) in enumerate(upper_columns_mapping):
                if rowspan == 2:
                    middle_columns_mapping.insert(index, ('', 1))
                elif rowspan == 3:
                    middle_columns_mapping.insert(index, ('', 1))
                    lower_columns_mapping.insert(index, ('', 1))
            for index, (_, rowspan) in enumerate(middle_columns_mapping):
                if rowspan == 2:
                    lower_columns_mapping.insert(index, ('', 1))
            column_names = concatenate_elements(upper_columns_mapping, middle_columns_mapping, lower_columns_mapping)
        case 2:
            upper_columns_mapping = []
            middle_columns_mapping = []
            upper_columns, middle_columns = column_list
            for column in upper_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                upper_columns_mapping.append(value)
            for column in middle_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                middle_columns_mapping.append(value)
            for index, (_, rowspan) in enumerate(upper_columns_mapping):
                if rowspan == 2:
                    middle_columns_mapping.insert(index, ('', 1))
            column_names = concatenate_elements(upper_columns_mapping, middle_columns_mapping)
        case _:
            return pd.DataFrame()
    df = []
    for row in driver.find_elements(By.XPATH, "//*[contains(@class, 'el-table__row')]"):
        values = []
        for value in row.find_elements(By.XPATH, './/td'):
            values.append(driver.execute_script("return arguments[0].innerText;", value))
        df.append(values)
    return pd.DataFrame(df, columns=column_names)

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)

    url = 'https://flageval.baai.ac.cn/#/trending'
    driver.get(url)
    
    language = driver.find_element(By.XPATH, '//i[@class="el-icon v-icon cursor-pointer hover-trigger el-tooltip__trigger el-tooltip__trigger"]')
    language.click()
    
    english = driver.find_elements(By.XPATH, '//li[@class="el-dropdown-menu__item"]')[1]
    english.click()
    
    for domain in driver.find_element(By.XPATH, '//div[@class="el-form-item__content"]').find_elements(By.XPATH, './/div'):
        domain_name = domain.text
        print(domain.text)
        if domain_name == 'NLP':
            continue
        domain.click()
        metric_list = driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[1].find_elements(By.XPATH, './/div')
        if metric_list:
            for metric in metric_list:
                metric_name = metric.text
                print(metric.text)
                metric.click()
                try:
                    for type in driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[2].find_elements(By.XPATH, './/div'):
                        type_name = type.text
                        print(type.text)
                        type.click()
                        # time.sleep(0.5)
                        df = retrieve_table(driver)
                        if not df.empty:
                            df.to_json(f'{path_leaderboard}/shw-{prepcess_name(domain_name)}-{prepcess_name(metric_name)}-{prepcess_name(type_name)}.json', orient='records', indent=4)
                except:
                    df = retrieve_table(driver)
                    if not df.empty:
                        df.to_json(f'{path_leaderboard}/shw-{prepcess_name(domain_name)}-{prepcess_name(metric_name)}.json', orient='records', indent=4)
                    print('No model types')
        else:
            df = retrieve_table(driver)
            if not df.empty:
                df.to_json(f'{path_leaderboard}/shw-{prepcess_name(domain_name)}.json', orient='records', indent=4)
            print('No metrics')
    