import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Ko Chatbot Arena Leaderboard"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://elo.instruct.kr/leaderboard'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table')
    column_names = [column.text for column in table.find_elements(By.XPATH, './/thead/tr/th')]

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = [value.text for value in row.find_elements(By.XPATH, './/td')]
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=['랭킹'], inplace=True)
    df.rename(columns={'모델 이름': 'Model'}, inplace=True)
    df.to_json(f'{path_leaderboard}/ip.json', orient='records', indent=4)
    