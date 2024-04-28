from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import conf

# Replace with your desired URL
URL = "https://www.aena.es/es/estadisticas/informes-mensuales.html?anio="
years_range = list(range(2014, 2024))

download_directory = "C:/Users/rober/OneDrive/Escriptori/DataSets/Time-Series/time-series/data"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory
})

# Initialize the webdriver (Chrome in this case)
driver = webdriver.Chrome(executable_path=conf.CHROME_DRIVER_PATH)

# Open the URL
for year in years_range:
    url = f"{URL}{year}"
    driver.get(url)

#  List all elements (might be overwhelming for complex pages)
# all_elements = driver.find_elements_by_tag_name("*")
# for element in all_elements:
#     print(element.tag_name)

# Define how to identify the element you want to click on
# Here we use By.ID, replace with your appropriate strategy (By.CLASS_NAME, By.XPATH etc.)
element_to_click = driver.find_element(By.ID, "specific_element_id")  # Replace with actual ID

# Click on the element
element_to_click.click()

# Do something after clicking (optional)
#  ... your code here ...

# Close the browser (optional)
# driver.quit()
