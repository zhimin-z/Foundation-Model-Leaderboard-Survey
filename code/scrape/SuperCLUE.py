import pandas as pd
import os

from selenium.webdriver.common.by import By
from seleniumbase import Driver

leaderboard_open = 'data/SuperCLUE-Open'


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
    leaderboards = driver.find_elements(By.XPATH, '//div[@id="component-228"]/div')
    
    for index, leaderboard in enumerate(leaderboards[0].find_elements(By.XPATH, './/button')):
        leaderboard_name = leaderboard.text.encode('ascii', 'ignore').decode('ascii')
        leaderboard_path = f"data/{leaderboard_name}"
        
        if not os.path.exists(leaderboard_path):
            os.makedirs(leaderboard_path)
            
        leaderboard.click()
    
        for subleaderboard in leaderboards[index + 1].find_elements(By.XPATH, ".//button"):
            subleaderboard_name = preprocess_text(subleaderboard)
            subleaderboard.click()
            
            column_names = [column.text for column in leaderboard_columns[iteration].find_elements(By.XPATH, './/tr/th')]
            
            df = []
            for row in leaderboard_tables[iteration].find_elements(By.XPATH, './/tr'):
                values = [value.text for value in row.find_elements(By.XPATH, './/td')]
                df.append(values)
                
            df = pd.DataFrame(df, columns=column_names)
            
            try:
                df.drop(columns=['排名'], inplace=True)
            except:
                pass
            
            df.rename(columns={'模型': 'Model', '模型名称': 'Model'}, inplace=True)
            df.to_json(f"{leaderboard_path}/ip-{subleaderboard_name}.json", orient='records', indent=4)
            
            if subleaderboard_name in ['十大基础能力排行榜', 'OPEN多轮开放问题排行榜']:
                if not os.path.exists(leaderboard_open):
                    os.makedirs(leaderboard_open)
                df.to_json(f"{leaderboard_open}/ip-{subleaderboard_name}.json", orient='records', indent=4)
            
            iteration += 1
            
    driver.quit()