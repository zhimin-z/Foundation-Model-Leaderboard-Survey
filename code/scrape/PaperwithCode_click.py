from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
import re

dataset = 'common-voice'
stop_link = 'automatic-speech-recognition-on-mozilla-65'

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    driver = uc.Chrome(options=chrome_options)
    base_url = 'https://paperswithcode.com'
    url = f'{base_url}/dataset/{dataset}'
    driver.get(url)
    
    leaderboard_links = []
    leaderboard_tables = driver.find_elements(By.XPATH, '//table[@id="benchmarks-table"]/tbody/tr')
    for leaderboard in leaderboard_tables:
        text = leaderboard.get_attribute('onclick')
        match = re.findall(r"'(.*?)'", text)[0]
        if stop_link and (stop_link in match):
            break
        link = f'{base_url}{match}'
        leaderboard_links.append(link)

    for url in leaderboard_links:
        driver.execute_script(f"window.open('{url}');")
    
    time.sleep(100000)
                