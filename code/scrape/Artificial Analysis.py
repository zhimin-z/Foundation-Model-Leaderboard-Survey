from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver as uc
import pandas as pd
import os

path_leaderboard = ['LLM API Hosts Leaderboard', 'Models Leaderboard']
suffix_leaderboard = ['hosts', 'models']
    
parallel_queries = ['single', 'multiple']
prompt_length = ['short', 'long']

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)
    
    base_url = 'https://artificialanalysis.ai/leaderboards'
    for path, suffix in zip(path_leaderboard, suffix_leaderboard):
        path = 'data/' + path
        if not os.path.exists(path):
            os.makedirs(path)
            
        for query in parallel_queries:
            for length in prompt_length:
                url = f'{base_url}/{suffix}?parallel_queries={query}&prompt_length={length}'
                driver.get(url)
                
                expand_columns = driver.find_element(By.XPATH, '//div[@class="flex items-center py-4"]/button')
                expand_columns.click()
            
                table = driver.find_element(By.XPATH, '//table[@class="w-full caption-bottom text-sm rounded"]')
                upper_columns, lower_columns = table.find_elements(By.XPATH, './/thead/tr')
                lower_column_list = [lower_column.text for lower_column in lower_columns.find_elements(By.XPATH, './/th')]
                
                column_names = []
                for upper_column in upper_columns.find_elements(By.XPATH, './/th'):
                    for _ in range(int(upper_column.get_attribute('colspan'))):
                        if upper_column.text:
                            column_names.append(f'{lower_column_list.pop(0)} ({upper_column.text})')
                        else:
                            column_names.append(lower_column_list.pop(0))
            
                df = []
                for row in table.find_elements(By.XPATH, '//tbody/tr'):
                    values = []
                    for index, value in enumerate(row.find_elements(By.XPATH, './/td')):
                        if index == len(column_names) - 1:
                            values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                        else:
                            values.append(value.text)
                    df.append(values)
            
                df = pd.DataFrame(df, columns=column_names)
                df.rename(columns={'MODEL': 'Model'}, inplace=True)
                df.to_json(f'{path}/iw-{suffix}-{query}-{length}.json', orient='records', indent=4)
                    