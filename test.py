import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


proxy_hosts = '66.29.129.54'
proxy_ports = '31983'

chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}:{1}'.format(proxy_hosts, proxy_ports))
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.google.com.pk/')
time.sleep(5)
driver.find_element(By.XPATH, '//textarea[@id="APjFqb"]').send_keys('what percentage does ken nugent take')
time.sleep(5)
driver.find_element(By.XPATH, '//textarea[@id="APjFqb"]').send_keys(Keys.ENTER)
time.sleep(10)
flag = False
while flag == False:
    links = driver.find_elements(By.XPATH, '//div[@id="search"]//div[@class="Z26q7c UK95Uc jGGQ5e"]//a')
    for link in links:
        if 'firmslaws' in link.get_attribute('href'):
            print(link.get_attribute('href'))
            driver.get(link.get_attribute('href'))
            time.sleep(5)
            driver.find_element(By.XPATH, '//a[@title="Home"]').click()
            time.sleep(5)
            post_lst = []
            posts = driver.find_elements(By.XPATH, '//div[@id="sidebar-right"]//ul[@class="wp-block-latest-posts__list wp-block-latest-posts"]/li/a')
            for post in posts:
                post_lst.append(post.get_attribute('href'))
            for i in range(2):
                driver.get(post_lst[i])
                for i in range(5):
                    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(2)
            post_lst.clear()
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.HOME)
            time.sleep(3)
            driver.find_element(By.XPATH, '//a[@title="Home"]').click()
            time.sleep(5)
            posts = driver.find_elements(By.XPATH, '//div[@class="bs-blog-post list-blog"]/article/h4/a')
            for post in posts:
                post_lst.append(post.get_attribute('href'))
            for i in range(2):
                driver.get(post_lst[i])
                for i in range(5):
                    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(2)
            post_lst.clear()
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.HOME)
            time.sleep(3)
            driver.find_element(By.XPATH, '//a[@title="Real estate laws"]').click()
            time.sleep(5)
            posts = driver.find_elements(By.XPATH, '//div[@class="bs-blog-post list-blog"]/article/h4/a')
            for post in posts:
                post_lst.append(post.get_attribute('href'))
            for i in range(2):
                driver.get(post_lst[i])
                for i in range(5):
                    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(2)
            post_lst.clear()

            break
        else:
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
            time.sleep(2)

    try:
        driver.find_element(By.XPATH, '//div[@class="GNJvt ipz2Oe"]').click()
        print('here')
    except:
        try:
            driver.find_element(By.XPATH, '//span[@class="RVQdVd"]').click()
            print('Here')
        except:
            next_page = driver.find_element(By.XPATH, '//td[@class="d6cvqb BBwThe"][2]/a')
            # driver.get(next_page.get_attribute('href'))
            next_page.click()
            time.sleep(5)
            