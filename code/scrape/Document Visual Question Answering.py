import pandas as pd
import time
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Document Visual Question Answering"


def preprocess_text(s):
    s = s.lower()
    s = s.split(' - ')[-1]
    s = s.replace(' ', '_')
    return s

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    url = 'https://rrc.cvc.uab.es/?ch=17&com=evaluation'
    driver.get(url)
    
    leaderboard_names = []
    leaderboard_urls = []
    for task in driver.find_elements(By.XPATH, '//li[contains(@class, "pill ")]'):
        name = preprocess_text(task.text)
        url = task.find_element(By.XPATH, './/a').get_attribute('href')
        leaderboard_names.append(name)
        leaderboard_urls.append(url)
    
    for name, url in zip(leaderboard_names, leaderboard_urls):
        driver.get(url)
        time.sleep(5)
        
        table = driver.find_element(By.XPATH, '//table[@id="table-1-1"]')
        
        try:
            upper_columns, lower_columns = table.find_elements(By.XPATH, './/thead/tr')
            lower_column_list = [lower_column.text for lower_column in lower_columns.find_elements(By.XPATH, './/th')]

            column_names = []
            for upper_column in upper_columns.find_elements(By.XPATH, './/th'):
                for _ in range(int(upper_column.get_attribute('colspan'))):
                    if upper_column.text:
                        column_names.append(f'{upper_column.text} ({lower_column_list.pop(0)})')
                    elif lower_column_list[0]:
                        column_names.append(lower_column_list.pop(0))
                    else:
                        lower_column_list.pop(0)
        except:
            column_names = []
            for upper_column in table.find_elements(By.XPATH, './/thead/tr/th'):
                if upper_column.text:
                    column_names.append(upper_column.text)
        
        df = []
        for row in table.find_elements(By.XPATH, './/tbody/tr'):
            values = []
            for value in row.find_elements(By.XPATH, './/td'):
                if value.text:
                    values.append(value.text)
            df.append(values)
                    
        df = pd.DataFrame(df, columns=column_names)
        df.rename(columns={'Method': 'Model'}, inplace=True)
        df.to_json(f"{path_leaderboard}/ip-{name}.json", orient='records', indent=4)
