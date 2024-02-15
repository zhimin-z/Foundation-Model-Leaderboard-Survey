from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/Provider Leaderboard"
    
output_token_length_list = {
    'short': 100,
    'long': 1000,
}
service_load_list = {
    'small': 2,
    'medium': 20,
    'large': 50,
}

output_token_length_list_inverse = {v: k for k, v in output_token_length_list.items()}
service_load_list_inverse = {v: k for k, v in service_load_list.items()}

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
    
    driver = uc.Chrome()
    driver.implicitly_wait(10)
    
    base_url = 'https://leaderboard.withmartian.com'
    driver.get(base_url)
    
    for output_token_length in output_token_length_list_inverse:
        for service_load in service_load_list_inverse:
            url = f'{base_url}/?output_tokens={output_token_length}&num_concurrent_request={service_load}&selected_models=llama2-70b-chat%2Cmixtral-8x7b%2COpenAI+models%2CAnthropic+models'
            driver.get(url)
            
            column_names = []
            for column in driver.find_elements(By.XPATH, '//div[@class="tr"]/div'):
                if column.text.strip():
                    column_names.append(column.text)
                else:
                    column_names.append('Link')
            
            df = []
            for row in driver.find_elements(By.XPATH, '//div[@role="rowgroup"]/div'):
                values = []
                elements = row.find_elements(By.XPATH, './/div[@role="cell"]')
                for index, value in enumerate(elements):
                    if index == len(elements) - 1:
                        values.append(value.find_element(By.XPATH, './/a').get_attribute('href'))
                    else:
                        values.append(value.text)
                df.append(values)
            
            df = pd.DataFrame(df, columns=column_names)
            df.rename(columns={'PROVIDER': 'Model'}, inplace=True)
            df.to_json(f'{path_leaderboard}/shw-{output_token_length_list_inverse[output_token_length]}-{service_load_list_inverse[service_load]}.json', orient='records', indent=4)
                    