from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd
import os

path_leaderboard = "data/CMB"

if __name__ == '__main__':
    if not os.path.exists(path_leaderboard):
        os.makedirs(path_leaderboard)
        
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://cmedbenchmark.llmzoo.com/static/leaderboard.html'
    driver.get(url)

    df = []
    column_names = []
    for index, row in enumerate(driver.find_elements(By.XPATH, '//div[@class="table-container"]/table/tbody/tr')):
        if index == 0:
            column_names_primary = []
            for column in row.find_elements(By.XPATH, './/th'):
                try:
                    column_names_primary.append(
                        (column.text, int(column.get_attribute('colspan'))))
                except:
                    column_names_primary.append((column.text, 1))
        elif index == 1:
            column_names_secondary = [
                column.text for column in row.find_elements(By.XPATH, './/td')]
            for name, span in column_names_primary:
                if span > 1:
                    for _ in range(span):
                        column_names.append(
                            name + '_' + column_names_secondary.pop(0))
                else:
                    column_names.append(name)
        else:
            values = []
            for index2, value in enumerate(row.find_elements(By.XPATH, './/td')):
                if index2 == 1:
                    values.append(
                        f"[{value.text}]({value.find_element(By.XPATH, './/a').get_attribute('href')})")
                else:
                    values.append(value.text)
            df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    leaderboard_names = [
        leaderboard.text for leaderboard in driver.find_elements(By.XPATH, '//h2')]
    df.to_json(f"{path_leaderboard}/iw-{leaderboard_names.pop(0).replace('CMB-', '').lower()}.json",
               orient='records', indent=4)

    column_names = []
    for column in driver.find_elements(By.XPATH, '//table[@class="results"]/thead/tr/th'):
        column_names.append(column.text)

    df = []
    for row in driver.find_elements(By.XPATH, '//table[@class="results"]/tbody/tr'):
        values = [value.text for value in row.find_elements(By.XPATH, './/td')]
        df.append(values)

    df = pd.DataFrame(df, columns=column_names)
    df.to_json(f"{path_leaderboard}/iw-{leaderboard_names.pop(0).replace('CMB-', '').lower()}.json",
               orient='records', indent=4)
