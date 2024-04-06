import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Indic LLM Leaderboard"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    url = 'https://cognitive-lab-indic-llm-leaderboard.hf.space'
    driver.get(url)
    
    df = []
    for index, row in enumerate(driver.find_elements(By.XPATH, '//tr[@role="row"]')):
        if index:
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        else:
            column_names = [column.text for column in row.find_elements(By.XPATH, './/th')]
            
    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=[''], inplace=True)
    df.to_json(f'{path_leaderboard}/hf.json', orient='records', indent=4)

    driver.quit()
