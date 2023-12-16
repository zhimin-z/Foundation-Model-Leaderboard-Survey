import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import csv
import json
import re

# Set up the Selenium WebDriver
driver = uc.Chrome()  # Replace with the browser you're using
url = 'https://mmmu-benchmark.github.io/'  # Replace with the path to your HTML file
driver.get(url)

# Extract the JavaScript data
script_element = driver.find_element(By.TAG_NAME, 'script')
script = driver.execute_script("return arguments[0].textContent;", script_element)
matches = re.findall(r'data: (\{.*?\}),\s*options:', script, re.DOTALL)

# Check if matches were found
if matches:
    data_json = matches[0]

    # Parse the JSON data
    data = json.loads(data_json)
    datasets = data['datasets']

    # Prepare the CSV data
    csv_data = [['Model', 'Easy', 'Medium', 'Hard', 'Overall']]
    for dataset in datasets:
        row = [dataset['label']]
        row.extend(dataset['data'])
        csv_data.append(row)

    # Save the data to a CSV file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

# Close the browser
driver.quit()
