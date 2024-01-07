from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/MINT-Bench"

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://xingyaoww.github.io/mint-bench'
    driver.get(url)
    
    column_names = []
    table = driver.find_element(By.XPATH, '//div[@id="benchmark-table"]')
    for column in table.find_elements(By.XPATH, './/div[@class="tabulator-headers"]/div'):
        column_name = column.find_element(By.XPATH, './/div[@class="tabulator-col-title"]').text
        subcolumns = column.find_elements(By.XPATH, './/div[@class="tabulator-col-group-cols"]/div')
        if subcolumns:
            for subcolumn in subcolumns:
                subcolumn_text = subcolumn.find_element(By.XPATH, './/div[@class="tabulator-col-title"]').text
                column_names.append(f'{column_name} ({subcolumn_text})')
        else:
            column_names.append(column_name)
    print(column_names)
    
    df = []
    for row in table.find_elements(By.XPATH, './/div[@class="tabulator-table"]/div'):
        values = [value.text for value in row.find_elements(By.XPATH, './/div')[:len(column_names)]]
        df.append(values)
    
    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Model Family': 'Model'}, inplace=True)
    df.to_json(f'{path_leaderboard}/gh.json', orient='records', indent=4)