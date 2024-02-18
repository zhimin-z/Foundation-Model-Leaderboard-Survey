from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import pickle
import time
import os

path_leaderboard = "data/HELM Classic"
url = 'https://crfm.stanford.edu/helm/classic/latest/#/leaderboard'
# group_excluded = ['core scenarios', 'targeted evaluations']
table_excluded = ['general information']


def preprocess_name(s):
    s = s.lower().replace("/", "_").replace(" - ",
                                            "_").replace(": ", "_").replace(" ", "_")
    return s


def save(path_leaderboard, group_name, table_name):
    with open(f'{path_leaderboard}/checkpoint.pkl', 'wb') as file:
        checkpoint = {'group': group_name, 'scenario': table_name}
        pickle.dump(checkpoint, file)


def load(path_leaderboard):
    try:
        with open(f'{path_leaderboard}/checkpoint.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}


def remove(path_leaderboard):
    os.remove(f'{path_leaderboard}/checkpoint.pkl')


def scrape_data(driver, url, path_leaderboard, checkpoint):
    driver.get(url)
    select = Select(driver.find_element(
        By.XPATH, '//select[@name="group" and @id="group"]'))
    for option in select.options[::-1]:
        if not checkpoint:
            select.select_by_visible_text(option.text)
            time.sleep(1)
            scenarios = driver.find_elements(
                By.XPATH, '//div[@role="navigation"]/div')
            if scenarios:
                for scenario in scenarios[::-1]:
                    save(path_leaderboard, option.text, scenario.text)
                    scenario.click()
                    time.sleep(1)
                    process_table(driver, option.text,
                                  scenario.text, path_leaderboard)
            else:
                save(path_leaderboard, option.text, '')
                process_table(driver, option.text, '', path_leaderboard)
        elif checkpoint and (option.text == checkpoint['group']):
            select.select_by_visible_text(option.text)
            time.sleep(1)
            if checkpoint['scenario']:
                for scenario in driver.find_elements(By.XPATH, '//div[@role="navigation"]/div')[::-1]:
                    if not checkpoint:
                        save(path_leaderboard, option.text, scenario.text)
                        scenario.click()
                        time.sleep(1)
                        process_table(driver, option.text,
                                      scenario.text, path_leaderboard)
                    elif scenario.text == checkpoint['scenario']:
                        scenario.click()
                        time.sleep(1)
                        process_table(driver, option.text,
                                      scenario.text, path_leaderboard)
                        checkpoint = {}
            else:
                process_table(driver, option.text, '', path_leaderboard)
                checkpoint = {}


def process_table(driver, group_name, table_name, path_leaderboard):
    # if group_name.lower() in group_excluded:
    #     return
    if table_name.lower() in table_excluded:
        return
    table = driver.find_element(
        By.XPATH, f'//table[@class="table w-full px-4"]')
    column_names = [column.text for column in table.find_elements(
        By.XPATH, './/th/div/span')]
    df = [[value.text for value in row.find_elements(
        By.XPATH, './/td')] for row in table.find_elements(By.XPATH, './/tbody/tr')]
    df = pd.DataFrame(df, columns=column_names)
    file_name = f'{path_leaderboard}/iw-{preprocess_name(group_name)}'
    if table_name:
        file_name += f'-{preprocess_name(table_name)}'
    df.to_json(f'{file_name}.json', orient='records', indent=4)


if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    checkpoint = load(path_leaderboard)

    while True:
        try:
            scrape_data(driver, url, path_leaderboard, checkpoint)
            print("Done!")
            break
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            checkpoint = load(path_leaderboard)
            driver.refresh()

    remove(path_leaderboard)
