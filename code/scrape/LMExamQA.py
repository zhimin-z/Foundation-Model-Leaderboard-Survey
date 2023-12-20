from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

from pathlib import Path

from selenium.webdriver.chrome.options import Options
import os
import time

options = Options()
download_path = Path("data/LMExamQA")
options.add_experimental_option("prefs", {
    "download.default_directory": str(download_path),
    "download.prompt_for_download": False,
    # "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

def get_latest_file(dir_path):
    files = os.listdir(dir_path)
    paths = [os.path.join(dir_path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def download(driver, menu):
    menu.click()
    time.sleep(0.2)
    # wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    # try:
    #     menu = driver.find_element(By.XPATH, '//button[@class="highcharts-a11y-proxy-element highcharts-no-tooltip"]')
    # except:
    #     menu = driver.find_element(By.XPATH, '//div[@class="highcharts-contextmenu"]')
    # menu.click()
    # # menu = driver.find_element(By.XPATH, '//g[@class="highcharts-exporting-group"]')
    # # except:
    # #     menu = driver.find_element(By.XPATH, '//g[@class="highcharts-no-tooltip highcharts-button highcharts-contextbutton highcharts-button-normal"]')
    # #     menu.click()
    # table = driver.find_elements(By.XPATH, '//li[@class="highcharts-menu-item"]')[6]
    # print(table.text)
    # table.click()

if __name__ == '__main__':
    driver = uc.Chrome()#options=options)
    driver.implicitly_wait(5)

    base_url = 'https://lmexam.com/'
    driver.get(base_url)
    
    result = driver.find_element(By.XPATH, '//button[@id="pills-result-tab"]')
    download(driver, result)
    # time.sleep(10)  # Adjust sleep time as needed
    # original_file_name = os.path.join(download_path, "original_file_name.ext")
    # new_file_name = os.path.join(download_path, "new_file_name.ext")
    # os.rename(original_file_name, new_file_name)
    
    for domain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-primary"]'):
        print(domain.text)
        download(driver, domain)
        # time.sleep(1)
        for subdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-danger"]'):
            print(subdomain.text)
            download(driver, subdomain)
            # time.sleep(1)
            for subsubdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-warning"]'):
                print(subsubdomain.text)
                download(driver, subsubdomain)
                # time.sleep(1)
                for subsubsubdomain in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-success"]'):
                    print(subsubsubdomain.text)
                    download(driver, subsubsubdomain)
