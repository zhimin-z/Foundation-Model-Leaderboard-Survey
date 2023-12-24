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


def concatenate_elements(*args):
    return '\n'.join(filter(None, args))

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
        domain.click()
        metric_list = driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[1].find_elements(By.XPATH, './/div')
        if metric_list:
            for metric in metric_list:
                metric_name = metric.text
                print(metric.text)
                metric.click()
                try:
                    # type_list = driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[2].find_elements(By.XPATH, './/div')
                    for type in driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[2].find_elements(By.XPATH, './/div'):
                        type_name = type.text
                        print(type.text)
                        type.click()
                        time.sleep(0.5)
                        
                        upper_columns_mapping = []
                        middle_columns_mapping = []
                        upper_columns_list = []
                        middle_columns_list = []
                        lower_columns_list = []
                        column_list = driver.find_elements(By.XPATH, '//thead[@class="is-group"]/tr')
                        match len(column_list):
                            case 3:
                                upper_columns, middle_columns, lower_columns = column_list
                                for column in upper_columns.find_elements(By.XPATH, './/th'):
                                    value = (driver.execute_script("return arguments[0].innerText;", column), column.get_attribute('colspan'))
                                    upper_columns_mapping.append(value)
                                for column in middle_columns.find_elements(By.XPATH, './/th'):
                                    value = (driver.execute_script("return arguments[0].innerText;", column), column.get_attribute('colspan'))
                                    middle_columns_mapping.append(value)
                                for column in lower_columns.find_elements(By.XPATH, './/th'):
                                    lower_columns_list.append(driver.execute_script("return arguments[0].innerText;", column))
                                for name, frequency in upper_columns_mapping:
                                    upper_columns_list.extend([name] * int(frequency))
                                for name, frequency in middle_columns_mapping:
                                    middle_columns_list.extend([name] * int(frequency))
                                middle_columns_list = [''] * (len(upper_columns_list) - len(middle_columns_list)) + middle_columns_list
                                lower_columns_list = [''] * (len(upper_columns_list) - len(lower_columns_list)) + lower_columns_list
                                column_names = [concatenate_elements(a, b, c) for a, b, c in zip(upper_columns_list, middle_columns_list, lower_columns_list)]
                            case 2:
                                upper_columns, lower_columns = column_list
                                for column in upper_columns.find_elements(By.XPATH, './/th'):
                                    value = (driver.execute_script("return arguments[0].innerText;", column), column.get_attribute('colspan'))
                                    upper_columns_mapping.append(value)
                                for column in lower_columns.find_elements(By.XPATH, './/th'):
                                    lower_columns_list.append(driver.execute_script("return arguments[0].innerText;", column))
                                for name, frequency in upper_columns_mapping:
                                    upper_columns_list.extend([name] * int(frequency))
                                lower_columns_list = [''] * (len(upper_columns_list) - len(lower_columns_list)) + lower_columns_list
                                column_names = [concatenate_elements(a, b) for a, b in zip(upper_columns_list, lower_columns_list)]
                            case _:
                                print('No data!')
                        df = []
                        for row in driver.find_elements(By.XPATH, "//*[contains(@class, 'el-table__row')]"):
                            values = []
                            for value in row.find_elements(By.XPATH, './/td'):
                                values.append(driver.execute_script("return arguments[0].innerText;", value))
                            df.append(values)
                        df = pd.DataFrame(df, columns=column_names)
                        df.to_json(f'{path_leaderboard}/shw-{prepcess_name(domain_name)}-{prepcess_name(metric_name)}-{prepcess_name(type_name)}.json', orient='records', indent=4)
                except:
                    print('No model types')
        else:
            print('No metrics')
    