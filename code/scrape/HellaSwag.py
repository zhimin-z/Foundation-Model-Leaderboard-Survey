from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/HellaSwag"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://rowanzellers.com/hellaswag'
    driver.get(url)
    
    df = []
    for index, row in enumerate(driver.find_elements(By.XPATH, '//table[@class="table performanceTable box-shadow"]/tbody/tr')):
        if index:
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        else:
            column_names = [column.text for column in row.find_elements(By.XPATH, './/th')]
        
    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Rank': 'Date'}, inplace=True)
    df['Date'] = df['Date'].apply(lambda x: x.split('\n')[-1])
    df.to_json(f'{path_leaderboard}/shw.json', orient='records', indent=4)
