from selenium.webdriver.common.by import By
# import undetected_chromedriver as uc
from selenium import webdriver as uc
import pandas as pd
import time
import re

from pathlib import Path

path_leaderboard = Path("data/Chatbot Arena Leaderboard")


def filter_string(text):
    regex_pattern = r'🤖|⭐|📈|📚|📊|🗳️'
    filtered_string = re.sub(regex_pattern, '', text)
    return filtered_string.strip()


def prepcess_name(s):
    s = s.lower()
    s = s.replace(' ', '_')
    return s


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://chat.lmsys.org'
    driver.get(url)
    time.sleep(10)

    leaderboard_button = driver.find_element(
        By.XPATH, '//div[@id="component-1"]/div[1]/button[4]')
    leaderboard_button.click()

    leaderboards = driver.find_element(By.XPATH, '//div[@id="component-105"]')
    for index, button in enumerate(leaderboards.find_elements(By.XPATH, ".//button[contains(@class, 'svelte-kqij2n')]")):
        leaderboard_name = prepcess_name(button.text)
        button.click()
        table = leaderboards.find_elements(
            By.XPATH, f'.//table[@class="svelte-1tclfmr"]')[index]
        column_names = []
        for column in table.find_elements(By.XPATH, './/thead/tr/th'):
            column_name = filter_string(column.text)
            column_names.append(column_name)
        df = []
        for row in table.find_elements(By.XPATH, './/tbody/tr'):
            values = [value.text for value in row.find_elements(
                By.XPATH, './/td')]
            df.append(values)
        df = pd.DataFrame(df, columns=column_names)
        if 'Rank' in df.columns:
            df = df.drop('Rank', axis=1)
        df.to_json(f'{path_leaderboard}/shw-{leaderboard_name}.json',
                   orient='records', indent=4)
