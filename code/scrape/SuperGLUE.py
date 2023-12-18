from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

from pathlib import Path

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = 'https://super.gluebenchmark.com/leaderboard'
    driver.get(url)
    
    column_names = []
    for column in driver.find_elements(By.XPATH, '//tr[@class="jss209 jss212"]/th')[2:]:
        column_names.append(column.text)
    
    df = []
    for submission in driver.find_elements(By.XPATH, '//tr[@class="jss209"]'):
        row = []
        for index, value in enumerate(submission.find_elements(By.XPATH, './/td')):
            if index < 2:
                continue
            elif index == 4:
                try:
                    link = value.find_element(By.XPATH, './/a').get_attribute('href')
                except:
                    link = None
                row.append(link)
            else:
                row.append(value.text)
        df.append(row)
        
    df = pd.DataFrame(df, columns=column_names)
    path_leaderboard = 'data/SuperGLUE/shw.json'
    df.to_json(path_leaderboard, orient='records', indent=4)