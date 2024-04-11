import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Red Teaming Resistance Benchmark"
leaderboard_names = ['content', 'dataset']

def extract_data(driver):
    df_merged = []
    for table in driver.find_elements(By.XPATH, '//table'):        
        df = []
        for row in table.find_elements(By.XPATH, './/tbody/tr'):
            values = [value.text for value in row.find_elements(By.XPATH, './/td')]
            df.append(values)
            
        column_names = [column.text for column in table.find_elements(By.XPATH, './/thead/tr/th')]
        df = pd.DataFrame(df, columns=column_names)
        df_merged.append(df)
        
    df_merged = pd.concat(df_merged, axis=1)
    df_merged.drop(columns=[''], inplace=True)
    df_merged.rename(columns={'Model Name': 'Model'}, inplace=True)
    df_merged.to_json(f'{path_leaderboard}/hf-{leaderboard_names.pop(0)}.json', orient='records', indent=4, index=False)

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://haizelabs.com/benchmarks/space'
    driver.get(url)
    
    extract_data(driver)
    
    button1 = driver.find_element(By.XPATH, '//div[@aria-controls="listbox-0"]')
    button1.click()
    button2 = driver.find_elements(By.XPATH, '//ul[@role="listbox"]/li')[-1]
    button2.click()
    
    extract_data(driver)