import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/LogicKor"
leaderboard_names = ['average', 'single_turn', 'multiple_turn']

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://lk.instruct.kr'
    driver.get(url)
    
    for button in driver.find_elements(By.XPATH, '//div[@role="group"]/button'):
        button.click()
        
        table = driver.find_element(By.XPATH, '//table')
        column_names = [column.text for column in table.find_elements(By.XPATH, './/th')]
        
        df = []
        for row in table.find_elements(By.XPATH, './/tr'):
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        
        df = pd.DataFrame(df, columns=column_names)
        df.dropna(subset=['모델명'], inplace=True)
        df.drop(columns=['순위', '평가로그'], inplace=True)
        df.rename(columns={'모델명': 'Model'}, inplace=True)
        df.to_json(f'{path_leaderboard}/ip-{leaderboard_names.pop(0)}.json', orient='records', indent=4)

    driver.quit()