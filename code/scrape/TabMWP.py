from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/TabMWP"

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)

    url = 'https://promptpg.github.io/leaderboard.html'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table[@class="js-sort-table"]')

    column_names = []
    for column in table.find_elements(By.XPATH, './/thead/tr/td'):
        column_names.append(column.text)

    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = [column.text for column in row.find_elements(By.XPATH, './/td')]
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=['#'], inplace=True)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
