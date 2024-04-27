from selenium import webdriver
from selenium.webdriver.common.by import By

# Replace with your desired URL
url = "https://www.example.com"

# Initialize the webdriver (Chrome in this case)
driver = webdriver.Chrome()

# Open the URL
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
