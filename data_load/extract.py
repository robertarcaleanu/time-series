from selenium import webdriver
from selenium.webdriver.common.by import By

import conf
import time

# Replace with your desired URL
URL = "https://www.aena.es/es/estadisticas/informes-mensuales.html?anio="
years_range = list(range(2004, 2025))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "C:\\Users\\rober\\OneDrive\\Escriptori\\DataSets\\Time-Series\\time-series\\data"}    )

# Initialize the webdriver (Chrome in this case)
driver = webdriver.Chrome(executable_path=conf.CHROME_DRIVER_PATH, chrome_options=chrome_options)

# maximize the window
driver.maximize_window()

i = 0
for year in years_range:
    url = f"{URL}{year}"
    driver.get(url)
    time.sleep(2)

    if i == 0:
        # click on accept cookies
        accept_cookies = driver.find_element(By.CSS_SELECTOR, "#modal_footer > div > div > div > button.ecix-bold.ecix-font-1-2em.elix-accordion-btn-primary")
        accept_cookies.click()
    
    list_reports = driver.find_elements(By.CSS_SELECTOR, "div[class='informes']")
    for report in list_reports:
        download_report = report.find_element(By.CSS_SELECTOR, "div[class='descargas']")
        download_report = download_report.find_elements(By.CSS_SELECTOR, "div[class='btn-download-pdf']")[1]
        
        # Adjust window to click on the download
        y_coordinate = download_report.location['y']
        adjusted_y_coordinate = y_coordinate - 500 
        driver.execute_script("window.scrollTo(0, arguments[0]);", adjusted_y_coordinate)

        time.sleep(1)
        download_report.click()
        
    print(f"Year {year} downloaded")
    time.sleep(2)
    i = i +1

# Close the browser (optional)
driver.quit()
