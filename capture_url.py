from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Set up Chrome with the desired options to enable DevTools
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: to run the browser in headless mode (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start the WebDriver (use the appropriate path for your ChromeDriver)
driver = webdriver.Chrome(options=options)

# Open the URL you want to inspect
url = "https://codes.iccsafe.org/content/NYNYCBC2022P1/chapter-1-administration"
driver.get(url)

# Wait for the page to load and any AJAX requests to complete (adjust as needed)
time.sleep(5)

# Start capturing network traffic
driver.execute_cdp_cmd('Network.enable', {})

# Function to handle network response and capture URLs
def capture_urls(request):
    if 'url' in request:
        print("Captured URL:", request['url'])
        
# Attach the function to the network response event
driver.request_interceptor = capture_urls

# Perform actions like clicking buttons or waiting for AJAX requests to complete

# Close the browser after data is captured
time.sleep(3)
driver.quit()
