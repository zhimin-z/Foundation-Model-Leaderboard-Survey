import time
import re

from selenium.webdriver.common.by import By
from seleniumbase import Driver

dataset = 'universal-dependencies'
stop_page = ''

if __name__ == '__main__':
    base_url = 'https://paperswithcode.com'
    url = f'{base_url}/dataset/{dataset}'
    
    driver = Driver(uc=True)
    driver.get(url)
    
    leaderboard_links = []
    leaderboard_tables = driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr')
    for leaderboard in leaderboard_tables:
        text = leaderboard.get_attribute('onclick')
        match = re.findall(r"'(.*?)'", text)[0]
        if stop_page and (stop_page in match):
            break
        link = f'{base_url}{match}'
        leaderboard_links.append(link)

    for url in leaderboard_links:
        driver.execute_script(f"window.open('{url}');")
    
    time.sleep(100000)
                