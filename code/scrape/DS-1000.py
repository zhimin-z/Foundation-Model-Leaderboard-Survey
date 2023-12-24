from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/DS-1000"

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)

    url = 'https://ds1000-code-gen.github.io'
    driver.get(url)

    df = []
    table = driver.find_elements(By.XPATH, '//table[@class="table performanceTable"]/tbody/tr')
    for index, row in enumerate(table):
        if index:
            values = [column.text for column in row.find_elements(By.XPATH, './/td')]
            df.append(values)
        else:
            column_names = [column.text for column in row.find_elements(By.XPATH, './/th')]
            
    df = pd.DataFrame(df, columns=column_names)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)
