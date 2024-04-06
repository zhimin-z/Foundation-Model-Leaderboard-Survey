from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumbase import Driver
import pandas as pd
import os

path_leaderboard = "data/LiveCodeBench"


def prepcess_name(s):
    s = s.lower()
    s = s.replace(' ', '_')
    return s


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = Driver(uc=True)
    driver.implicitly_wait(5)

    url = 'https://livecodebench.github.io/leaderboard.html'
    driver.get(url)
    
    # Locate the left slider handle
    slider = driver.find_element(By.XPATH, "//input[@aria-label='Date Slider']")
    actions = ActionChains(driver)
    actions.click_and_hold(slider).move_by_offset(-500, 0).release().perform()
    
    for button in driver.find_elements(By.XPATH, '//ul[@class="tabs "]/li'):
        leaderboard_name = prepcess_name(button.text)
        button.click()
        
        column_names = [column.text for column in driver.find_elements(By.XPATH, '//div[@class="ag-header-row ag-header-row-column"]/div')]
        
        df = []
        for row in driver.find_elements(By.XPATH, '//div[@class="ag-center-cols-container"]/div'):
            values = [column.text for column in row.find_elements(By.XPATH, './div')]
            df.append(values)
        
        df = pd.DataFrame(df, columns=column_names)
        df.drop(columns=['Rank'], inplace=True)
        df.to_json(f'{path_leaderboard}/gh-{leaderboard_name}.json', orient='records', indent=4)