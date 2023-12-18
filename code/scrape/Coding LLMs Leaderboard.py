from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = 'https://leaderboard.tabbyml.com'
    driver.get(url)
    
    column_names = ['']
    
    df = []
    for submission in driver.find_elements(By.XPATH, '//div[@class="flex flex-col"]/div'):
        model = submission.find_element(By.XPATH, './/p').text
        print(model)
        for value in submission.find_elements(By.XPATH, './/div/div'):
            print(value.find_element(By.TAG_NAME, 'span').text)
            # print(value.find_element(By.XPATH, './/span').text)
        
        
    # df = pd.DataFrame(df, columns=column_names)
    # path_leaderboard = 'data/SuperGLUE/shw.json'
    # df.to_json(path_leaderboard, orient='records', indent=4)