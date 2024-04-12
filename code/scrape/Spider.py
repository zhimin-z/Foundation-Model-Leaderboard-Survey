import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/Spider"


def prepcess_name(s):
    s = s.lower()
    s = s.replace('leaderboard - ', '')
    s = s.replace(' ', '_')
    return s


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://yale-lily.github.io/spider'
    driver.get(url)
    
    for leaderboard in driver.find_elements(By.XPATH, '//div[@class="col-md-7"]/div'):
        leaderboard_name = leaderboard.find_element(By.XPATH, './/div[@class="infoHeadline"]').text
        leaderboard_name = prepcess_name(leaderboard_name)
        df = []
        for index, row in enumerate(leaderboard.find_elements(By.XPATH, './/table[@class="table performanceTable"]/tbody/tr')):
            if index:
                values = [value.text for value in row.find_elements(By.XPATH, './/td')]
                df.append(values)
            else:
                column_names = [column.text for column in row.find_elements(By.XPATH, './/th')]
        
        df = pd.DataFrame(df, columns=column_names)
        df.rename(columns={'Rank': 'Date'}, inplace=True)
        df['Date'] = df['Date'].apply(lambda x: x.split('\n')[-1])
        df.to_json(f'{path_leaderboard}/gh-{leaderboard_name}.json', orient='records', indent=4)
        