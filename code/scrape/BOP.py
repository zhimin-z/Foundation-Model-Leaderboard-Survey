import pandas as pd
import os

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = "data/BOP"

tasks = ['pose-estimation-bop19', 'detection-bop22', 'segmentation-bop22', 'pose-estimation-unseen-bop23', 'detection-unseen-bop23', 'segmentation-unseen-bop23']
datasets = ['core-datasets', 'lm', 'lm-o', 't-less', 'itodd', 'hb', 'hope', 'ycb-v', 'ru-apc', 'ic-bin', 'ic-mi', 'tud-l', 'tyo-l']


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = Driver(uc=True)
    driver.implicitly_wait(10)

    base_url = 'https://bop.felk.cvut.cz/leaderboards'
    driver.get(base_url)
    
    for task in tasks:
        for dataset in datasets:
            url = f'{base_url}/{task}/{dataset}'
            driver.get(url)
            
            select = Select(driver.find_element(By.XPATH, '//select[@name="leaderboard_length"]'))
            select.select_by_visible_text('All')
        
            table = driver.find_element(By.XPATH, '//table[@id="leaderboard"]')
            column_names = [column.text for column in table.find_elements(By.XPATH, './/thead/tr/th') if column.text]
        
            df = []
            for row in table.find_elements(By.XPATH, './/tbody/tr'):
                values = [value.text for value in row.find_elements(By.XPATH, './/td')]
                df.append(values)
        
            try:
                df = pd.DataFrame(df, columns=column_names)
                df.rename(columns={'Method': 'Model', 'Submission': 'Model'}, inplace=True)
                df.to_json(f'{path_leaderboard}/ip-{task}-{dataset}.json', orient='records', indent=4)
            except:
                print(f'Empty leaderboard: {task}-{dataset}')
    
    driver.quit()