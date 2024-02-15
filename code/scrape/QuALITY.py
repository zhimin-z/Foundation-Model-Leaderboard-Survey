from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/QuALITY"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://nyu-mll.github.io/quality'
    driver.get(url)

    column_names = []
    column_names_backup = ['Date', 'Description']
    upper_columns, lower_columns = driver.find_elements(By.XPATH, '//thead[@class="thead-light"]/tr')
    lower_column_names = [column.text for column in lower_columns.find_elements(By.XPATH, './/th')]
    for column in upper_columns.find_elements(By.XPATH, './/th'):
        try:
            for _ in range(int(column.get_attribute('colspan'))):
                column_name = f'{lower_column_names.pop(0)} ({column.text})'
                column_names.append(column_name)
        except:
            if column.text:
                column_names.append(column.text)
            else:
                column_names.append(column_names_backup.pop(0))
                
    df = []
    for row in driver.find_elements(By.XPATH, '//table[@class="table table-responsive"]/tbody'):
        row_no_description, row_description = row.find_elements(By.XPATH, './/tr')
        values = []
        for name, value in zip(column_names, row_no_description.find_elements(By.XPATH, './/td')):
            if name == 'Paper':
                try:
                    values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                except:
                    values.append('')
            elif name == 'Code':
                try:
                    values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                except:
                    values.append('')
            elif name == 'Date':
                values.append(value.text.split('\n')[-1])
            elif name == 'Description':
                values.append(row_description.text)
            else:
                values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Model name': 'Model'}, inplace=True)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
