import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

all_internal_links = []
website_name = 'firmslaws'
# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://firmslaws.com/")
time.sleep(5)
linkss = driver.find_elements(By.TAG_NAME, 'a')
for i in linkss:
    href = i.get_attribute('href')
    # print('ye loop se pehle')
    # print(href)
    if "https://{}.com".format(website_name) in href:
        if '#' not in href:
            all_internal_links.append(href)
            print('ye rhe links')
print(all_internal_links)
# Execute JavaScript to open a new window
# driver.execute_script("window.open('about:blank','new_window')")
# time.sleep(2)
# # Switch to the newly opened window
# driver.switch_to.window(driver.window_handles[-2])
# time.sleep(2)
# driver.close()
# driver.switch_to.window(driver.window_handles[-1])
# # You can now interact with the new window
# driver.get("https://www.google.com")
while True:
    pass
# Rest of your code...
