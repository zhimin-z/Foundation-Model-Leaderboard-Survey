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


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)

    url = 'https://flageval.baai.ac.cn/#/trending'
    driver.get(url)
    
    language = driver.find_element(By.XPATH, '//i[@class="el-icon v-icon cursor-pointer hover-trigger el-tooltip__trigger el-tooltip__trigger"]')
    language.click()
    
    english = driver.find_elements(By.XPATH, '//li[@class="el-dropdown-menu__item"]')[1]
    english.click()
            
    # domain_list = Select()
    for domain in driver.find_element(By.XPATH, '//div[@class="el-form-item__content"]').find_elements(By.XPATH, './/div'):
        domain_name = domain.text
        print(domain.text)
        # domain_list.select_by_visible_text(domain_name)
        domain.click()
        # time.sleep(1)
        # driver.execute_script("arguments[0].click();", domain)
        metric_list = driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[1].find_elements(By.XPATH, './/div')
        if metric_list:
            print('Metrics:')
            for metric in metric_list:
                metric_name = metric.text
                print(metric.text)
                # metric_list.select_by_visible_text(metric_name)
                metric.click()
                # time.sleep(1)
                # driver.execute_script("arguments[0].click();", metric)
                type_list = driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[2].find_elements(By.XPATH, './/div')
                if type_list:
                    print('Model Types:')
                    for type in type_list:
                        type_name = type.text
                        print(type.text)
                        # type_list.select_by_visible_text(type_name)
                        type.click()
                        # time.sleep(1)
                        # driver.execute_script("arguments[0].click();", type)
                        column_names = []
                        upper_columns, lower_columns = driver.find_elements(By.XPATH, '//thead[@class="is-group"]/tr')
                        for column in upper_columns.find_elements(By.XPATH, './/th'):
                            if column.get_attribute('colspan') == '1':
                                column_names.append(column.text)
                        for column in lower_columns.find_elements(By.XPATH, './/th'):
                            column_names.append(column.text)
                        print(column_names)
                else:
                    print('No model types')
        else:
            print('No metrics')
    