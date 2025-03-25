from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
import random
import requests, re
from bs4 import BeautifulSoup


def get_proxies():
    regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
    c = requests.get("https://spys.me/proxy.txt")
    test_str = c.text
    a = re.finditer(regex, test_str, re.MULTILINE)
    with open("proxies_list.txt", 'w') as file:
        for i in a:
            print(i.group(),file=file)
            
    d = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(d.content, 'html.parser')
    td_elements = soup.select('.fpl-list .table tbody tr td')
    ips = []
    ports = []
    for j in range(0, len(td_elements), 8):
        ips.append(td_elements[j].text.strip())
        ports.append(td_elements[j + 1].text.strip())
    with open("proxies_list.txt", "a") as myfile:
        for ip, port in zip(ips, ports):
            proxy = f"{ip}:{port}"
            print(proxy, file=myfile)


def get_proxy_list():

    get_proxies()
    with open("proxies_list.txt", "r") as file:
        proxy_list =  file.readlines()
    
    for i in range(len(proxy_list)):
        proxy_list[i] = proxy_list[i].replace('\n', '')

    return proxy_list

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0"
    ]
    return random.choice(user_agents)

def get_random_headers():
    user_agent = get_random_user_agent()
    chrome_versions = ["110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120"]
    chrome_version = random.choice(chrome_versions)
    
    # List of possible language preferences
    languages = [
        "en-US,en;q=0.9",
        "en-GB,en;q=0.9",
        "en-CA,en;q=0.9",
        "en-AU,en;q=0.9",
        "en,en-US;q=0.9"
    ]

    headers = {
        "User-Agent": user_agent,
        "Accept": random.choice([
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "*/*"
        ]),
        "Accept-Language": random.choice(languages),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "sec-ch-ua": f'"Not_A Brand";v="8", "Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}"',
        "sec-ch-ua-mobile": random.choice(["?0", "?1"]),
        "sec-ch-ua-platform": random.choice(['"Windows"', '"macOS"', '"Linux"']),
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": random.choice(["none", "same-origin"]),
        "Sec-Fetch-User": "?1",
        "DNT": random.choice(["1", "0"]),
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": random.choice(["max-age=0", "no-cache"])
    }
    
    # Randomly add or remove some headers
    if random.random() > 0.5:
        headers["Pragma"] = "no-cache"
    if random.random() > 0.5:
        headers["Accept-CH"] = "Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version"
    
    return headers

def create_headers_extension(headers):
    """Create a Chrome extension to modify headers"""
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Headers Modifier",
        "permissions": [
            "webRequest",
            "webRequestBlocking",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    
    background_js = """
    var headers = %s;

    chrome.webRequest.onBeforeSendHeaders.addListener(
        function(details) {
            Object.keys(headers).forEach(function(key) {
                var found = false;
                for (var i = 0; i < details.requestHeaders.length; ++i) {
                    if (details.requestHeaders[i].name.toLowerCase() === key.toLowerCase()) {
                        details.requestHeaders[i].value = headers[key];
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    details.requestHeaders.push({name: key, value: headers[key]});
                }
            });
            return {requestHeaders: details.requestHeaders};
        },
        {urls: ["<all_urls>"]},
        ["blocking", "requestHeaders", "extraHeaders"]
    );
    """ % json.dumps(headers)

    extension_dir = "header_modifier"
    if not os.path.exists(extension_dir):
        os.makedirs(extension_dir)

    with open(f"{extension_dir}/manifest.json", "w") as f:
        f.write(manifest_json)
    with open(f"{extension_dir}/background.js", "w") as f:
        f.write(background_js)

    return extension_dir

def get_random_proxy():
    proxies = get_proxy_list()
    return random.choice(proxies)

def create_driver():
    # Generate random headers
    headers = get_random_headers()
    
    # Create the extension with random headers
    extension_dir = create_headers_extension(headers)
    
    # Get random proxy
    proxy_ip_port = get_random_proxy()
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy_ip_port}')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument(f'--load-extension={os.path.abspath(extension_dir)}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add random window size
    sizes = [(1366, 768), (1920, 1080), (1536, 864), (1440, 900), (1280, 720)]
    window_size = random.choice(sizes)
    chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    
    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(options=chrome_options)
    
    # Modify webdriver properties to avoid detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver, extension_dir

def main():
    max_retries = 3
    retry_delay = random.uniform(2, 5)  # Random delay between retries
    
    for attempt in range(max_retries):
        driver, extension_dir = create_driver()
        
        try:
            # Add random delay before request
            time.sleep(random.uniform(1, 3))
            
            # Navigate to the target website
            print("Attempting to access codes.iccsafe.org...")
            driver.get("https://codes.iccsafe.org/")
            
            # Wait for page to load with random delay
            time.sleep(random.uniform(8, 12))
            
            try:
                # Using XPath with text content
                signin_button = driver.find_element(
                    By.XPATH, "//button[.//h4[text()='Sign In']]"
                )
                
                # Optionally scroll into view (if needed)
                actions = ActionChains(driver)
                actions.move_to_element(signin_button).perform()
                
                # Click the button
                signin_button.click()
                print("Clicked on Sign In button successfully!")
            except Exception as e:
                print(f"Error: {e}")
            break  # If successful, break the retry loop
            
        except Exception as e:
            print(f"Error occurred on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:  # If not the last attempt
                print(f"Retrying in {retry_delay:.1f} seconds...")
                time.sleep(retry_delay)
            
        finally:
            driver.quit()
            # Clean up the extension directory
            import shutil
            shutil.rmtree(extension_dir)
            
if __name__ == "__main__":
    main()