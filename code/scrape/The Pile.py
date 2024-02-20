from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver as uc
import pandas as pd
import os

path_leaderboard = "data/The Pile"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://pile.eleuther.ai'
    driver.get(url)
    
    table = driver.find_element(By.XPATH, '//table[@class="content-table"]')
    column_names = [column.text for column in table.find_elements(By.XPATH, './/thead/tr/th')]

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = [column.text for column in row.find_elements(By.XPATH, './/td')]
        df.append(values)
            
    df = pd.DataFrame(df, columns=column_names)
    df['Rank'] = df['Rank'].apply(lambda x: x.split('\n')[-1])
    df.rename(columns={'Rank': 'Date'}, inplace=True)
    df.to_json(f'{path_leaderboard}/iw.json', orient='records', indent=4)
