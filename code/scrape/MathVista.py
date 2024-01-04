from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/MathVista"

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)

    url = 'https://mathvista.github.io'
    driver.get(url)

    leaderboards = driver.find_elements(By.XPATH, '//section[@class="section"]')[2]
    leaderboard_names = []
    for leaderboard_name in leaderboards.find_elements(By.XPATH, './/h2[@class="title is-3"]'):
        leaderboard_names.append(leaderboard_name.text.lower().replace('leaderboard on ', ''))
    
    for leaderboard_table in leaderboards.find_elements(By.XPATH, './/table[@class="js-sort-table"]'):
        column_names = []
        for column in leaderboard_table.find_elements(By.XPATH, './/thead/tr/td'):
            column_names.append(column.text)
        df = []
        for row in leaderboard_table.find_elements(By.XPATH, './/tbody/tr'):
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        df = pd.DataFrame(df, columns=column_names)
        df.drop(columns=['#'], inplace=True)
        df.to_json(f'{path_leaderboard}/gh-{leaderboard_names.pop(0)}.json', orient='records', indent=4)
