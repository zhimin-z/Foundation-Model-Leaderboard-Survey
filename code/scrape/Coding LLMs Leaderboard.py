from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

if __name__ == '__main__':
    driver = uc.Chrome()
    actions = ActionChains(driver)
    driver.implicitly_wait(5)
    
    url = 'https://leaderboard.tabbyml.com'
    driver.get(url)
    
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
    df.to_json('data/Coding LLMs Leaderboard/shw.json', orient='records', indent=4)
        
        
        
    # df = pd.DataFrame(df, columns=column_names)
    # path_leaderboard = 'data/SuperGLUE/shw.json'
    # df.to_json(path_leaderboard, orient='records', indent=4)