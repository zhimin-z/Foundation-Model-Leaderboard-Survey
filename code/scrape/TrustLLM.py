from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/TrustLLM"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://trustllmbenchmark.github.io/TrustLLM-Website/leaderboard.html'
    driver.get(url)
    
    leaderboard_names = [name.text.lower() for name in driver.find_elements(By.XPATH, '//div[@class="section"]/h2')]
    
    for leaderboard in driver.find_elements(By.XPATH, ".//table[contains(@id, 'table_')]"):
        column_names = []
        for column in leaderboard.find_elements(By.XPATH, './/thead/tr/th'):
            column_name = column.text.replace(' (↑)', '')
            column_names.append(column_name)
        
        df = []
        for row in leaderboard.find_elements(By.XPATH, './/tbody/tr'):
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'{path_leaderboard}/gh-{leaderboard_names.pop(0)}.json', orient='records', indent=4)
        