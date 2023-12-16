from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests

from pathlib import Path

path_llm = Path("data/LMExamQA")
chrome_options = uc.ChromeOptions()
prefs = {"download.default_directory" : str(path_llm)}
chrome_options.add_experimental_option("prefs", prefs)

def download(driver):
    table = driver.find_element(By.XPATH, '//li[@class="highcharts-menu-item"]')[6]
    table.click()

if __name__ == '__main__':
    driver = uc.Chrome()
    driver = uc.Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    base_url = 'https://lmexam.com/'
    driver.get(base_url)
    
    result = driver.find_element(By.XPATH, '//button[@id="pills-result-tab"]')
    result.click()
    download(driver)
    
    for domain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-primary"]'):
        domain.click()
        download(driver)
        for subdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-danger"]'):
            subdomain.click()
            download(driver)
            for subsubdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-warning"]'):
                subsubdomain.click()
                download(driver)
                for subsubsubdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-success"]'):
                    subsubsubdomain.click()
                    download(driver)
            
        