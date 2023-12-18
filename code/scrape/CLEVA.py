from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    
    url = 'http://www.lavicleva.com/#/homepage/table'
    driver.get(url)
    
    language_switcher = driver.find_element(By.XPATH, '//div[@class="container-content-top-right-e"]')
    driver.execute_script("arguments[0].click();", language_switcher)
    
    for table in driver.find_elements(By.XPATH, '//div[@class="home-content-graph-item"]'):
        # driver.execute_script("arguments[0].scrollLeft += 500", table)
        name = table.find_element(By.XPATH, './/div[@class="home-item-title"]').text
        header = table.find_element(By.XPATH, './/div[@class="el-table__header-wrapper"]')
        column_names = [column.text for column in header.find_elements(By.XPATH, './/div[@class="cell"]')]
        print(column_names)
        body = table.find_element(By.XPATH, './/div[@class="el-table__body-wrapper is-scrolling-left"]')
        df = []
        for row in body.find_elements(By.XPATH, "//*[contains(@class, 'el-table__row')]"):
            entry = []
            for value in row.find_elements(By.XPATH, './/div[@class="cell"]'):
                entry.append(value.text)
            df.append(entry)
        df = pd.DataFrame(df, columns=column_names)
        df.to_json(f'data/CLEVA/shw-{name}.json', orient='records', indent=4)
                
            
            
    #         for _ in range(NUMBER_OF_SCROLLS):
    # driver.execute_script("arguments[0].scrollLeft += SCROLL_INCREMENT", scrollable_element)
    # time.sleep(SCROLL_PAUSE)  # Pause to allow content to load
        
        
    # df = pd.DataFrame(df, columns=column_names)
    # path_leaderboard = 'data/SuperGLUE/shw.json'
    # df.to_json(path_leaderboard, orient='records', indent=4)