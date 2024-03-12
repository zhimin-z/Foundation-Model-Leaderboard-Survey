import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

def preprocess_text(name):
    return name.text.lower().replace('auto', '').replace('agent', '').replace('superclue-safety', '')

if __name__ == '__main__':
    driver = Driver(uc=True)
    driver.implicitly_wait(10)
    
    url = 'https://www.superclueai.com'
    driver.get(url)
    
    iteration = 0
    leaderboard_columns = driver.find_elements(By.XPATH, '//thead[@class="svelte-1tclfmr"]')
    leaderboard_tables = driver.find_elements(By.XPATH, '//tbody[@class="svelte-1tclfmr"]')
    leaderboards = driver.find_elements(By.XPATH, '//div[@id="component-204"]/div')
    
    for index, leaderboard in enumerate(leaderboards[0].find_elements(By.XPATH, './/button')):
        leaderboard_name = leaderboard.text.encode('ascii', 'ignore').decode('ascii')
        leaderboard_path = f"data/{leaderboard_name}"
        
        if not os.path.exists(leaderboard_path):
            os.makedirs(leaderboard_path)
            
        leaderboard.click()
    
        for subleaderboard in leaderboards[index + 1].find_elements(By.XPATH, ".//button"):
            subleaderboard_name = preprocess_text(subleaderboard)
            subleaderboard.click()
            
            df = []
            for row in leaderboard_tables[iteration].find_elements(By.XPATH, './/tr'):
                values = [value.text for value in row.find_elements(By.XPATH, './/td')]
                df.append(values)
                
            column_names = [column.text for column in leaderboard_columns[iteration].find_elements(By.XPATH, './/tr/th')]
            df = pd.DataFrame(df, columns=column_names)
            
            try:
                df.drop(columns=['排名'], inplace=True)
            except:
                pass
            
            try:
                df.rename(columns={'模型': 'Model'}, inplace=True)
            except:
                df.rename(columns={'模型名称': 'Model'}, inplace=True)
                
            df.to_json(f"{leaderboard_path}/iw-{subleaderboard_name}.json", orient='records', indent=4)
            
            iteration += 1