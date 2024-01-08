from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(10)
    
    url = 'https://www.superclueai.com'
    driver.get(url)
    
    iteration = 0
    leaderboard_names = []
    leaderboard_columns = driver.find_elements(By.XPATH, '//thead[@class="thead svelte-1jok1de"]')
    leaderboard_tables = driver.find_elements(By.XPATH, '//tbody[@class="tbody svelte-1jok1de"]')
    leaderboards = driver.find_elements(By.XPATH, '//div[@id="component-162"]/div')
    for index, leaderboard in enumerate(leaderboards[0].find_elements(By.XPATH, './/button')):
        leaderboard_name = leaderboard.text.encode('ascii', 'ignore').decode('ascii')
        leaderboard.click()
        time.sleep(5)
        for subleaderboard in leaderboards[index + 1].find_elements(By.XPATH, ".//button[contains(@class, 'svelte-kqij2n')]"):
            subleaderboard_name = subleaderboard.text.lower().replace('auto', '').replace('agent', '').replace('superclue-safety', '')
            subleaderboard.click()
            column_names = [column.text for column in leaderboard_columns[iteration].find_elements(By.XPATH, './/tr/th')]
            print(column_names)
            df = []
            for row in leaderboard_tables[iteration].find_elements(By.XPATH, './/tr'):
                values = [value.text for value in row.find_elements(By.XPATH, './/td')]
                df.append(values)
            df = pd.DataFrame(df, columns=column_names)
            try:
                df.drop(columns=['排名'], inplace=True)
            except:
                pass
            df.rename(columns={'模型': 'Model'}, inplace=True)
            df.to_json(f"data/{leaderboard_name}/shw-{subleaderboard_name}.json", orient='records', indent=4)
            iteration += 1