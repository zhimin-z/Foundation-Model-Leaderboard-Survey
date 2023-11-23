from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import json

from pathlib import Path

path_llm = Path("data/llm")


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    base_url = 'https://paperswithcode.com'
    url = f'{base_url}/sota/sentence-completion-on-hellaswag'
    driver.get(url)
    
    table = driver.find_element(By.XPATH, '//script[@id="evaluation-table-data"]').get_attribute("innerText")
    table = json.loads(table)
    df = pd.DataFrame()
    
    for row in table:
        entry = {
            'Model': row['method'],
            'Accuracy': row['raw_metrics']['Accuracy'],
            'Paper': f'{base_url}{row["paper"]["url"]}',
            'Date': row['evaluation_date'],
        }
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    
    df.to_json(path_llm / 'HellaSwag-sentence_completion-paperwithcode-latest.json', orient='records', indent=4)
                