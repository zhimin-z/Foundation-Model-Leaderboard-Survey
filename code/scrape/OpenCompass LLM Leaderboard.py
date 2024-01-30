from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/OpenCompass LLM Leaderboard (v2)"


def preprocess_name(name):
    name = name.lower()
    name = name.replace(' ', '_')
    return name


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://rank.opencompass.org.cn/leaderboard-llm-v2'
    driver.get(base_url)
    
    index = 1
    while True:
        try:
            button = driver.find_element(By.XPATH, f'//div[@data-node-key="tab{index}"]/div')
            leaderboard_name = preprocess_name(button.text)
            button.click()
        
            column_names = []
            head = driver.find_elements(By.XPATH, f'//thead[@class="ant-table-thead"]')[index-1]
            for column in head.find_elements(By.XPATH, f'.//tr/th'):
                if column.text.strip():
                    column_names.append(column.text)
                else:
                    column_names.append(column.get_attribute('aria-label'))
            
            df = []
            body = driver.find_elements(By.XPATH, f'//tbody[@class="ant-table-tbody"]')[index-1]
            for row in body.find_elements(By.XPATH, f'.//tr')[1:]:
                values = [column.text for column in row.find_elements(By.XPATH, './/td')[1:]]
                df.append(values)
            
            df = pd.DataFrame(df, columns=column_names)
            df.to_json(f'{path_leaderboard}/shw-{leaderboard_name}.json', orient='records', indent=4)
            
            index += 1
        except:
            break
