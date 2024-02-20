from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/InfographicVQA"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://rrc.cvc.uab.es/?ch=17&com=evaluation&task=3'
    driver.get(url)

    table = driver.find_element(By.XPATH, '//table[@id="table-1-1"]')
    upper_columns, lower_columns = table.find_elements(By.XPATH, './/thead/tr')
    column_names = []
    for upper_column in upper_columns.find_elements(By.XPATH, './/th'):
        colspan = int(upper_column.get_attribute('colspan'))
        lower_column_list = [lower_column.text for lower_column in lower_columns.find_elements(By.XPATH, './/th')]
        if colspan > 0:
            for _ in range(colspan):
                if upper_column.text:
                    column_names.append(f'{upper_column.text} ({lower_column_list.pop(0)})')
                elif lower_column_list[0]:
                    column_names.append(lower_column_list.pop(0))
                
        # else:
        #     column_names.append(upper_column.text)
    
    df = []
    for row in table.find_elements(By.XPATH, './/tbody/tr'):
        values = []
        for value in row.find_elements(By.XPATH, './/td'):
            values.append(value.text)
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.rename(columns={'Method': 'Model'}, inplace=True)
    df.to_json(f"{path_leaderboard}/iw.json", orient='records', indent=4)
