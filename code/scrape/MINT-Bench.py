from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/MINT-Bench"
leaderboard_names = ['multi_turn_interactions', 'natural_language_feedback']

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://xingyaoww.github.io/mint-bench'
    driver.get(url)
    
    table = driver.find_element(By.XPATH, f'//div[@id="benchmark-table"]')
    column_names = []
    for column in table.find_elements(By.XPATH, './/div[@class="tabulator-headers"]/div'):
        column_name = column.find_element(By.XPATH, './/div[@class="tabulator-col-title"]').text
        subcolumns = column.find_elements(By.XPATH, './/div[@class="tabulator-col-group-cols"]/div')
        if subcolumns:
            for subcolumn in subcolumns:
                subcolumn_text = subcolumn.find_element(By.XPATH, './/div[@class="tabulator-col-title"]').text
                column_names.append(f'{column_name} ({subcolumn_text})')
        else:
            column_names.append(column_name)
        
    df = []
    for row in table.find_elements(By.XPATH, './/div[@class="tabulator-table"]/div'):
        values = [value.text for value in row.find_elements(By.XPATH, './div')[:-1]]
        df.append(values)
    
    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Model Family': 'Model'}, inplace=True)
    df.to_json(f'{path_leaderboard}/iw-{leaderboard_names.pop(0)}.json', orient='records', indent=4)
    
    table = driver.find_element(By.XPATH, f'//div[@id="benchmark-feedback-efficancy-table"]')
    column_names = []
    for column in table.find_elements(By.XPATH, './/div[@class="tabulator-headers"]/div'):
        column_name = column.find_element(By.XPATH, './/div[@class="tabulator-col-title"]').text
        subcolumns = column.find_elements(By.XPATH, './/div[@class="tabulator-col-group-cols"]/div')
        if subcolumns:
            for subcolumn in subcolumns:
                subcolumn_text = subcolumn.find_element(By.XPATH, './/div[@class="tabulator-col-title"]').text
                column_names.append(subcolumn_text)
        else:
            column_names.append(column_name)
        
    df = []
    for row in table.find_elements(By.XPATH, './/div[@class="tabulator-table"]/div'):
        values = [value.text for value in row.find_elements(By.XPATH, './div')]
        df.append(values)
    
    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Model Family': 'Model'}, inplace=True)
    df.to_json(f'{path_leaderboard}/iw-{leaderboard_names.pop(0)}.json', orient='records', indent=4)