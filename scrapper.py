from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Ensure the output directory exists
os.makedirs("data", exist_ok=True)

# Queries for scraping
queries = [
    "chapter-1-administration",
    "chapter-r2-definitions",
    "chapter-r3-general-requirements",
    "chapter-r4-residential-energy-efficiency",
]

# Your login credentials
email = "your_email@example.com"
password = "your_password"

# Initialize the WebDriver
driver = webdriver.Chrome()

# Function to log in
def log_in():
    try:
        # Wait for the email field and input email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emailAddress"))
        )
        email_field.send_keys(email)

        # Locate the password field (adjust locator if needed)
        password_field = driver.find_element(By.NAME, "password")  # Replace with actual identifier if available
        password_field.send_keys(password)

        # Locate and click the login button
        login_button = driver.find_element(
            By.CLASS_NAME, "v-btn--contained"
        )  # Adjust locator if needed
        login_button.click()

        print("Login successful.")
    except Exception as e:
        print(f"Login failed: {e}")

# Iterate over each query and fetch the HTML
for query in queries:
    url = f"https://codes.iccsafe.org/content/OHEC2017P1/{query}"
    try:
        # Fetch the webpage
        driver.get(url)
        
        # Log in before accessing the content
        log_in()

        # Wait for the main content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "v-main"))
        )

        # Find the elements and save their HTML
        elems = driver.find_elements(By.CLASS_NAME, "v-main")
        print(f"{len(elems)} elements found for query '{query}'")

        for elem in elems:
            d = elem.get_attribute("outerHTML")
            with open(f"data/{query}.html", "w", encoding="utf-8") as f:
                f.write(d)

    except Exception as e:
        print(f"Error occurred for query '{query}': {e}")
    
    time.sleep(4)  # Respectful delay between requests

# Close the WebDriver
driver.quit()



# def click_sign_in_button():
#     try:
#         # Wait for the button to be clickable
#         sign_in_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "v-btn--flat"))
#         )
#         # Click the button
#         sign_in_button.click()
#         print("Sign In button clicked successfully.")
#     except Exception as e:
#         print(f"Failed to click Sign In button: {e}")
        

# email = "sahilgoregaonkar123@gmail.com"
# password = "CZs59Nq$7Aq*BK8"  
    
# def log_in():
#     try:
#         # Wait for the email field and input email
#                     email_field = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.ID, "emailAddress"))
#                     )
#                     email_field.send_keys(email)

#                     # Locate the password field (adjust locator if needed)
#                     password_field = driver.find_element(By.NAME, "password")  # Replace with actual identifier if available
#                     password_field.send_keys(password)

#                     # Locate and click the login button
#                     login_button = driver.find_element(
#                         By.CLASS_NAME, "v-btn--contained"
#                     )  # Adjust locator if needed
#                     login_button.click()

#                     print("Login successful.")
#     except Exception as e:
#             print(f"Login failed: {e}")

