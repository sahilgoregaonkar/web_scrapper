from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

queries = [
    "-ny-chapter-1-scope-and-administration",
    "chapter-2-definitions",
    "chapter-3-general-regulations",
    "chapter-4-gas-piping-installations",
    "chapter-5-chimneys-and-vents",
    "chapter-6-specific-appliances",
    "chapter-7-gaseous-hydrogen-systems",
    "chapter-8-referenced-standards",
    "appendix-a-sizing-and-capacities-of-gas-piping",
    "appendix-b-sizing-of-venting-systems-serving-appliances-equipped-with-draft-hoods-category-i-appliances-and-appliances-listed-for-use-with-type-b-vents",
    "appendix-d-recommended-procedure-for-safety-inspection-of-an-existing-appliance-installation",
]

# Ensure the "data" directory exists
if not os.path.exists(r"C:\Users\Admin\Desktop\web-scrapper\data"):
    os.makedirs("data")

# Step 2: Iterate over each query and fetch the HTML
for query in queries:
    url = f"https://codes.iccsafe.org/content/NYSFGC2020P1/{query}"
    driver.get(url)

    # Wait for the main content to be loaded (adjust this selector based on the actual page structure)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "v-main"))
        )
    except Exception as e:
        print(f"Error loading page for {query}: {e}")
        continue  # Skip this page if there's an issue

    # Find the main content element
    elems = driver.find_elements(By.CLASS_NAME, "v-main")
    print(f"{len(elems)} elements found for {query}")

    # Check if the 'data' directory exists and create it if it doesn't
    file_path = f"data/{query}.html"

    # Ensure the file name is safe by sanitizing the query (remove slashes or invalid characters)
    file_path = file_path.replace("/", "_").replace(":", "_")

    # Write the page HTML content to a file
    for elem in elems:
        d = elem.get_attribute("outerHTML")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(d)
            print(f"Saved HTML for {query} to {file_path}")
        except Exception as e:
            print(f"Error saving HTML for {query}: {e}")

    # Wait a few seconds before moving to the next page
    time.sleep(4)

driver.quit()  # Close the WebDriver
