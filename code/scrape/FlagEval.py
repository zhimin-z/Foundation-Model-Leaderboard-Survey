from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/FlagEval"


def prepcess_name(s):
    s = s.lower()
    s = s.replace(" - ", "_")
    s = s.replace(": ", "_")
    s = s.replace(" ", "_")
    return s


def expand_list_by_column(input_list):
    expanded_list = []
    for element in input_list:
        element_name, colspan, rowspan = element
        for _ in range(colspan):
            expanded_list.append((element_name, rowspan))
    return expanded_list


def concatenate_elements(*expanded_lists):
    concatenated_results = []
    extracted_elements = [[elem[0] for elem in lst] for lst in expanded_lists]
    for i in range(len(expanded_lists[0])):
        elements = [extracted_elements[j][i] for j in range(
            len(expanded_lists)) if extracted_elements[j][i]]
        concatenated_results.append("\n".join(elements))
    return concatenated_results


def retrieve_table(driver):
    column_list = driver.find_elements(
        By.XPATH, '//thead[@class="is-group"]/tr')
    match len(column_list):
        case 3:
            upper_columns_mapping = []
            middle_columns_mapping = []
            lower_columns_mapping = []
            upper_columns, middle_columns, lower_columns = column_list
            for column in upper_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(
                    column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                upper_columns_mapping.append(value)
            for column in middle_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(
                    column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                middle_columns_mapping.append(value)
            for column in lower_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(
                    column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                lower_columns_mapping.append(value)
            upper_columns_mapping = expand_list_by_column(
                upper_columns_mapping)
            middle_columns_mapping = expand_list_by_column(
                middle_columns_mapping)
            lower_columns_mapping = expand_list_by_column(
                lower_columns_mapping)
            for index, (_, rowspan) in enumerate(upper_columns_mapping):
                if rowspan == 2:
                    middle_columns_mapping.insert(index, ('', 1))
                elif rowspan == 3:
                    middle_columns_mapping.insert(index, ('', 1))
                    lower_columns_mapping.insert(index, ('', 1))
            for index, (_, rowspan) in enumerate(middle_columns_mapping):
                if rowspan == 2:
                    lower_columns_mapping.insert(index, ('', 1))
            column_names = concatenate_elements(
                upper_columns_mapping, middle_columns_mapping, lower_columns_mapping)
        case 2:
            upper_columns_mapping = []
            middle_columns_mapping = []
            upper_columns, middle_columns = column_list
            for column in upper_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(
                    column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                upper_columns_mapping.append(value)
            for column in middle_columns.find_elements(By.XPATH, './/th'):
                value = (driver.execute_script("return arguments[0].innerText;", column), int(
                    column.get_attribute('colspan')), int(column.get_attribute('rowspan')))
                middle_columns_mapping.append(value)
            upper_columns_mapping = expand_list_by_column(
                upper_columns_mapping)
            middle_columns_mapping = expand_list_by_column(
                middle_columns_mapping)
            for index, (_, rowspan) in enumerate(upper_columns_mapping):
                if rowspan == 2:
                    middle_columns_mapping.insert(index, ('', 1))
            column_names = concatenate_elements(
                upper_columns_mapping, middle_columns_mapping)
        case _:
            return pd.DataFrame()
    df = []
    for row in driver.find_elements(By.XPATH, "//*[contains(@class, 'el-table__row')]"):
        values = []
        for value in row.find_elements(By.XPATH, './/td'):
            values.append(driver.execute_script(
                "return arguments[0].innerText;", value))
        df.append(values)
    return pd.DataFrame(df, columns=column_names)


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)

    url = 'https://flageval.baai.ac.cn/#/trending'
    driver.get(url)

    language = driver.find_element(
        By.XPATH, '//i[@class="el-icon v-icon cursor-pointer hover-trigger el-tooltip__trigger el-tooltip__trigger"]')
    language.click()

    english = driver.find_elements(
        By.XPATH, '//li[@class="el-dropdown-menu__item"]')[1]
    english.click()

    for domain in driver.find_element(By.XPATH, '//div[@class="el-form-item__content"]').find_elements(By.XPATH, './/div'):
        domain.click()
        domain_name = domain.text
        for level1 in driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[1].find_elements(By.XPATH, './/div'):
            level1.click()
            level1_name = level1.text
            try:
                for level2 in driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[2].find_elements(By.XPATH, './/div'):
                    level2.click()
                    level2_name = level2.text
                    try:
                        raise Exception
                        # for level3 in driver.find_elements(By.XPATH, '//div[@class="el-form-item__content"]')[3].find_elements(By.XPATH, './/div'):
                        #     level3.click()
                        #     level3_name = level3.text
                        #     df = retrieve_table(driver)
                        #     if not df.empty:
                        #         df.rename(columns={'Model name': 'Model'}, inplace=True)
                        #         df.to_json(
                        #             f'{path_leaderboard}/shw-{prepcess_name(domain_name)}-{prepcess_name(level1_name)}-{prepcess_name(level2_name)}-{prepcess_name(level3_name)}.json', orient='records', indent=4)
                    except:
                        df = retrieve_table(driver)
                        if not df.empty:
                            df.rename(columns={'Model name': 'Model'}, inplace=True)
                            df.to_json(
                                f'{path_leaderboard}/shw-{prepcess_name(domain_name)}-{prepcess_name(level1_name)}-{prepcess_name(level2_name)}.json', orient='records', indent=4)
            except:
                df = retrieve_table(driver)
                if not df.empty:
                    df.rename(columns={'Model name': 'Model'}, inplace=True)
                    df.to_json(
                        f'{path_leaderboard}/shw-{prepcess_name(domain_name)}-{prepcess_name(level1_name)}.json', orient='records', indent=4)
