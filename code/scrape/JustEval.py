from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import pandas as pd

path_leaderboard = "data/JustEval"


def prepcess_name(s):
    s = s.lower()
    s = s.replace(' (', '_')
    s = s.replace(')', '')
    return s


if __name__ == '__main__':
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    url = 'https://allenai.github.io/re-align/just_eval.html'
    driver.get(url)

    index = 1
    while True:
        try:
            button = driver.find_element(
                By.XPATH, f'//button[@data-target="table{index}"]')
            leaderboard_name = prepcess_name(button.text)
            button.click()
            table = driver.find_element(By.XPATH, f'//div[@id="table{index}"]')
            column_names = [column.text.strip() for column in table.find_elements(
                By.XPATH, f'.//thead/tr/th')]
            df = []
            for row in table.find_elements(By.XPATH, f'.//tbody/tr'):
                values = [value.text.strip()
                          for value in row.find_elements(By.XPATH, f'.//td')]
                df.append(values)
            df = pd.DataFrame(df, columns=column_names)
            df.rename(columns={'Name': 'Model'}, inplace=True)
            df.to_json(
                f"{path_leaderboard}/gh-{leaderboard_name}.json", orient='records', indent=4)
            index += 1
        except:
            break
