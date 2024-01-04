from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = 'https://super.gluebenchmark.com/leaderboard'
    driver.get(url)
    
    column_names = []
    for column in driver.find_elements(By.XPATH, '//tr[@class="jss209 jss212"]/th')[1:]:
        column_names.append(column.text)
    
    df = []
    for submission in driver.find_elements(By.XPATH, '//tr[@class="jss209"]'):
        row = []
        for name, value in zip(column_names, submission.find_elements(By.XPATH, './/td')[1:]):
            if name == 'URL':
                try:
                    link = value.find_element(By.XPATH, './/a').get_attribute('href')
                except:
                    link = ''
                row.append(link)
            elif name == 'Name':
                if submission.get_attribute('style') == 'display: none;':
                    row.append(last_name)
                else:
                    last_name = value.text.split('\n')[-1]
                    row.append(last_name)
            else:
                row.append(value.text.split('\n')[-1])
        
        df.append(row)
        
    df = pd.DataFrame(df, columns=column_names)
    df.drop(columns=['Rank'], inplace=True)
    df.to_json('data/SuperGLUE/shw.json', orient='records', indent=4)