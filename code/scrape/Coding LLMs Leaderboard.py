import pandas as pd
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumbase import Driver

path_leaderboard = 'data/CCEval'
leaderboard_names = ['overall', 'instruct_fine_tuning', 'model_type']

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    actions = ActionChains(driver)
    driver.implicitly_wait(5)
    
    url = 'https://leaderboard.tabbyml.com'
    driver.get(url)
    
    for leaderboard in driver.find_elements(By.XPATH, '//div[@class="xl:fixed xl:bottom-0 my-10 flex flex-col gap-4 xl:flex-row"]/div'):
        leaderboard.click()
    
        column_names = ['Model']
        for column_name in driver.find_elements(By.XPATH, '//div[@class="flex flex-col font-thin"]/div'):
            column_names.append(column_name.text)
    
        models = driver.find_elements(By.XPATH, '//p[@class="font-sf tracking-wide md:w-48 md:mr-6 md:text-right"]')
        perfs = driver.find_elements(By.XPATH, './/div[@class="text-xs py-1 xl:py-0"]')
        df = []
        for model, perf in zip(models, perfs):
            actions.move_to_element(perf).perform()
            row = [model.text]
            for value in perf.find_elements(By.XPATH, ".//*[contains(@class, 'flex items-center gap-2')]"):
                row.append(value.text)
            df.append(row)
    
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'{path_leaderboard}/ip-{leaderboard_names.pop(0)}.json', orient='records', indent=4)