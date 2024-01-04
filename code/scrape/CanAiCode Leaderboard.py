from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import time

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    base_url = 'https://huggingface.co/spaces/mike-ravkine/can-ai-code-results'
    driver.get(base_url)
    
    for language in driver.find_elements(By.XPATH, '//label[@data-baseweb="radio"]')[1:]:
        # driver.execute_script("arguments[0].click();", language)
        print(language.get_attribute("value"))
        language.click()
        time.sleep(1)
        
        # df = []
        # for row in driver.find_elements(By.XPATH, '//div[@class="el-table__fixed-body-wrapper"]/table/tbody/tr'):
        #     entries = []
        #     for entry in row.find_elements(By.XPATH, './/td'):
        #         entries.append(entry.text)
        #     df.append(entries)
        # df = pd.DataFrame(df)
        # df.to_csv(f'data/CanAiCode Leaderboard/{language.get_attribute("value")}.csv', index=False, header=False)
    
    
    # full_results = driver.find_element(By.XPATH, "//input[@aria-label='Best Result Only']")
    # full_results.click()
    
    # time.sleep(1000)