from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from pathlib import Path

path_llm = Path("data/LMExamQA")
# from selenium.webdriver.chrome.service import Service
# chrome_options = uc.ChromeOptions()
# prefs = {
#     "download.default_directory": str(path_llm),
#     "download.prompt_for_download": False,
#     "safebrowsing.enabled": True,
# }
# chrome_options.add_experimental_option("prefs", prefs)
# service = Service()

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download(driver):
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="highcharts-a11y-proxy-element highcharts-no-tooltip"]')))
    menu.click()
    table = driver.find_elements(By.XPATH, '//li[@class="highcharts-menu-item"]')[6]
    table.click()

if __name__ == '__main__':
    driver = uc.Chrome()#service=service, options=chrome_options)
    driver.implicitly_wait(5)

    base_url = 'https://lmexam.com/'
    driver.get(base_url)
    
    result = driver.find_element(By.XPATH, '//button[@id="pills-result-tab"]')
    result.click()
    download(driver)
    
    for domain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-primary"]'):
        print(domain.text)
        domain.click()
        download(driver)
        for subdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-danger"]'):
            print(subdomain.text)
            subdomain.click()
            download(driver)
            for subsubdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-warning"]'):
                print(subsubdomain.text)
                subsubdomain.click()
                download(driver)
                for subsubsubdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-success"]'):
                    print(subsubsubdomain.text)
                    subsubsubdomain.click()
                    download(driver)
        