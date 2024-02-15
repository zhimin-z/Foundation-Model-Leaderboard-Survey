from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/TAT-DQA"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://nextplusplus.github.io/TAT-DQA'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table[@class="table well"]')
    column_names = [column.text for column in table.find_elements(By.XPATH, './/thead/tr/th')]

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for name, value in zip(column_names, row.find_elements(By.XPATH, './/td')):
            if name in ['Paper', 'Codes']:
                if value.text in ['Paper', 'Code']:
                    values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                else:
                    values.append(value.text)
            else:
                values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=['Rank'], inplace=True)
    df.rename(columns={'Model Name': 'Model'}, inplace=True)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
    