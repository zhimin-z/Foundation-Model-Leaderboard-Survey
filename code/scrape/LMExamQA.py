from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os
import time

def preprocess_name(s):
    return ' '.join(s.lower().split[:-1])

path_leaderboard = "data/LMExamQA"

def get_latest_file(dir_path):
    files = os.listdir(dir_path)
    paths = [os.path.join(dir_path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def download(driver, table):
    table.click()
    menu = driver.find_element(By.XPATH, '//button[@class="highcharts-a11y-proxy-element highcharts-no-tooltip"]')
    menu.click()
    download = driver.find_elements(By.XPATH, '//li[@class="highcharts-menu-item"]')[6]
    download.click()
    time.sleep(5)
    latest_file = get_latest_file(path_leaderboard)
    os.rename(latest_file, f'{path_leaderboard}/shw-{preprocess_name(table.text)}.csv')


if __name__ == '__main__':
    driver = uc.Chrome()

    params = {
        "behavior": "allow",
        "downloadPath": path_leaderboard
    }
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    driver.implicitly_wait(5)

    base_url = 'https://lmexam.com/'

    # driver.execute_cdp_cmd(
    #     "Browser.grantPermissions",
    #     {
    #         "origin": base_url,
    #         "permissions": ["geolocation"]
    #     },
    # )

    driver.get(base_url)

    zero = driver.find_element(By.XPATH, '//button[@id="pills-result-tab"]')
    download(driver, zero)

    for first in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-primary"]'):
        download(driver, first)
        for second in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-danger"]'):
            download(driver, second)
            for third in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-warning"]'):
                download(driver, third)
                for fourth in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-success"]'):
                    download(driver, fourth)
                    for fifth in driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-info"]'):
                        download(driver, fifth)
