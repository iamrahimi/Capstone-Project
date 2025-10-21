
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# --- Setup Chrome WebDriver ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Example parent page (list of years) ---
main_url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(main_url)
time.sleep(2)

# Get list of year links
year_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='yearly/']")
years_data = []

for link in year_links[:3]:  # scrape only 3 years for demo
    year_text = link.text.strip()
    year_url = link.get_attribute("href")
    if year_text.isdigit():
        years_data.append({"year": int(year_text), "url": year_url})

# Save the parent list of years
pd.DataFrame(years_data).to_csv("csv/main_years.csv", index=False)
print(" Saved main_years.csv")

# Folder to save sub CSVs
os.makedirs("tables", exist_ok=True)

# --- Loop through each year page ---
for y in years_data:
    year = y["year"]
    url = y["url"]
    print(f"\n Scraping tables for year {year} ...")
    driver.get(url)
    time.sleep(3)
    # Find all tables
    tables = driver.find_elements(By.CLASS_NAME, "ba-table")

    for idx, table in enumerate(tables):
        # Extract header
        title_h2 = table.find_element(By.TAG_NAME, "h2").text
        title_p = table.find_element(By.TAG_NAME, "p").text
        title_df = pd.DataFrame({"Title": [title_h2], "subtitle": [title_p]})

        # print(f"Table {idx+1}: {title_h2} - {title_p}")
   
        headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]

        # Extract rows
        rows = []
        for tr in table.find_elements(By.TAG_NAME, "tr"):
            cells = [td.text.strip() for td in tr.find_elements(By.TAG_NAME, "td")]
            if cells:
                rows.append(cells)

        if not rows:
            continue  # skip empty tables

        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers if headers else None)
        df["year"] = year  # relational key

        # Save each table separately
        table_name = title_h2.replace(" ", "_").lower()
        file_name = f"tables/{table_name}.csv"
        df.to_csv(file_name, index=False)
        print(f"Saved {file_name}")

driver.quit()
print("\nAll done! Each table saved under 'tables/' folder.")