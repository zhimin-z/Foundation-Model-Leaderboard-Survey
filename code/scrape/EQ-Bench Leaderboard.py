from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver as uc
import pandas as pd
import os

path_leaderboard = "data/EQ-Bench Leaderboard"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://eqbench.com'
    driver.get(url)
    
    df = []
    while True:
        table = driver.find_element(By.XPATH, '//table[@id="leaderboard"]')
        column_names = [column.text for column in table.find_elements(By.XPATH, './/thead/tr/th')]
        for row in table.find_elements(By.XPATH, './/tbody/tr'):
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
    
        next = driver.find_element(By.XPATH, '//li[@id="leaderboard_next"]')
        if 'disabled' in next.get_attribute('class'):
            break
        driver.execute_script("arguments[0].click();", next)
            
    df = pd.DataFrame(df, columns=column_names)
    df.to_json(f'{path_leaderboard}/iw.json', orient='records', indent=4)
