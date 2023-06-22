from django.shortcuts import render
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import pytz
from selenium.common.exceptions import WebDriverException
import subprocess
from fake_useragent import UserAgent
import logging

logging.getLogger('page_load_metrics_update_dispatcher').setLevel(logging.ERROR)
logging.getLogger('ssl_client_socket_impl').setLevel(logging.WARNING)



country_timezones = {'Afghanistan': 'Afghanistan Standard Time', 'Åland Islands': 'FLE Standard Time', 'Albania': 'Central Europe Standard Time', 'Algeria': 'W. Central Africa Standard Time', 'American Samoa': 'UTC-11', 'Andorra': 'W. Europe Standard Time', 'Angola': 'W. Central Africa Standard Time', 'Anguilla': 'SA Western Standard Time', 'Antarctica': 'Pacific SA Standard Time', 'Antigua and Barbuda': 'SA Western Standard Time', 'Argentina': 'Argentina Standard Time', 'Armenia': 'Caucasus Standard Time', 'Aruba': 'SA Western Standard Time', 'Australia': 'AUS Eastern Standard Time', 'Austria': 'W. Europe Standard Time', 'Azerbaijan': 'Azerbaijan Standard Time', 'Bahamas, The': 'Eastern Standard Time', 'Bahrain': 'Arab Standard Time', 'Bangladesh': 'Bangladesh Standard Time', 'Barbados': 'SA Western Standard Time', 'Belarus': 'Belarus Standard Time', 'Belgium': 'Romance Standard Time', 'Belize': 'Central America Standard Time', 'Benin': 'W. Central Africa Standard Time', 'Bermuda': 'Atlantic Standard Time', 'Bhutan': 'Bangladesh Standard Time', 'Bolivarian Republic of Venezuela': 'Venezuela Standard Time', 'Bolivia': 'SA Western Standard Time', 'Bonaire, Sint Eustatius and Saba': 'SA Western Standard Time', 'Bosnia and Herzegovina': 'Central European Standard Time', 'Botswana': 'South Africa Standard Time', 'Bouvet Island': 'UTC', 'Brazil': 'E. South America Standard Time', 'British Indian Ocean Territory': 'Central Asia Standard Time', 'Brunei': 'Singapore Standard Time', 'Bulgaria': 'FLE Standard Time', 'Burkina Faso': 'Greenwich Standard Time', 'Burundi': 'South Africa Standard Time', 'Cabo Verde': 'Cape Verde Standard Time', 'Cambodia': 'SE Asia Standard Time', 'Cameroon': 'W. Central Africa Standard Time', 'Canada': 'Eastern Standard Time', 'Cayman Islands': 'SA Pacific Standard Time', 'Central African Republic': 'W. Central Africa Standard Time', 'Chad': 'W. Central Africa Standard Time', 'Chile': 'Pacific SA Standard Time', 'China': 'China Standard Time', 'Christmas Island': 'SE Asia Standard Time', 'Cocos (Keeling) Islands': 'Myanmar Standard Time', 'Colombia': 'SA Pacific Standard Time', 'Comoros': 'E. Africa Standard Time', 'Congo': 'W. Central Africa Standard Time', 'Congo (DRC)':'W. Central Africa Standard Time', 'Cook Islands': 'Hawaiian Standard Time', 'Costa Rica': 'Central America Standard Time', "Côte d'Ivoire": 'Greenwich Standard Time', 'Croatia': 'Central European Standard Time', 'Cuba': 'Eastern Standard Time', 'Curaçao': 'SA Western Standard Time', 'Cyprus': 'E. Europe Standard Time', 'Czech Republic': 'Central Europe Standard Time', 'Democratic Republic of Timor-Leste': 'Tokyo Standard Time', 'Denmark': 'Romance Standard Time', 'Djibouti': 'E. Africa Standard Time', 'Dominica': 'SA Western Standard Time', 'Dominican Republic': 'SA Western Standard Time', 'Ecuador': 'SA Pacific Standard Time', 'Egypt': 'Egypt Standard Time', 'El Salvador': 'Central America Standard Time', 'Equatorial Guinea': 'W. Central Africa Standard Time', 'Eritrea': 'E. Africa Standard Time', 'Estonia': 'FLE Standard Time', 'Ethiopia': 'E. Africa Standard Time', 'Falkland Islands (Islas Malvinas)': 'SA Eastern Standard Time', 'Faroe Islands': 'GMT Standard Time', 'Fiji Islands': 'Fiji Standard Time', 'Finland': 'FLE Standard Time', 'France': 'Romance Standard Time', 'French Guiana': 'SA Eastern Standard Time', 'French Polynesia': 'Hawaiian Standard Time', 'French Southern and Antarctic Lands': 'West Asia Standard Time', 'Gabon': 'W. Central Africa Standard Time', 'Gambia, The': 'Greenwich Standard Time', 'Georgia': 'Georgian Standard Time', 'Germany': 'W. Europe Standard Time', 'Ghana': 'Greenwich Standard Time', 'Gibraltar': 'W. Europe Standard Time', 'Greece': 'GTB Standard Time', 'Greenland': 'Greenland Standard Time', 'Grenada': 'SA Western Standard Time', 'Guadeloupe': 'SA Western Standard Time', 'Guam': 'West Pacific Standard Time', 'Guatemala': 'Central America Standard Time', 'Guernsey': 'GMT Standard Time', 'Guinea': 'Greenwich Standard Time', 'Guinea-Bissau': 'Greenwich Standard Time', 'Guyana': 'SA Western Standard Time', 'Haiti': 'Eastern Standard Time', 'Heard Island and McDonald Islands': 'Mauritius Standard Time', 'Honduras': 'Central America Standard Time', 'Hong Kong SAR': 'China Standard Time', 'Hungary': 'Central Europe Standard Time', 'Iceland': 'Greenwich Standard Time', 'India': 'India Standard Time', 'Indonesia': 'SE Asia Standard Time', 'Iran': 'Iran Standard Time', 'Iraq': 'Arabic Standard Time', 'Ireland': 'GMT Standard Time', 'Israel': 'Israel Standard Time', 'Italy': 'W. Europe Standard Time', 
'Jamaica': 'SA Pacific Standard Time', 'Jan Mayen': 'W. Europe Standard Time', 'Japan': 'Tokyo Standard Time', 'Jersey': 'GMT Standard Time', 'Jordan': 'Jordan Standard Time', 'Kazakhstan': 'Central Asia Standard Time', 'Kenya': 'E. Africa Standard Time', 'Kiribati': 'UTC+12', 'Korea': 'Korea Standard Time', 'Kosovo': 'Central European Standard Time', 'Kuwait': 'Arab Standard Time', 'Kyrgyzstan': 'Central Asia Standard Time', 'Laos': 'SE Asia Standard Time', 'Latvia': 'FLE Standard Time', 'Lebanon': 'Middle East Standard Time', 'Lesotho': 'South Africa Standard Time', 'Liberia': 'Greenwich Standard Time', 'Libya': 'E. Europe Standard Time', 'Liechtenstein': 'W. Europe Standard Time', 'Lithuania': 'FLE Standard Time', 'Luxembourg': 'W. Europe Standard Time', 'Macao SAR': 'China Standard Time', 'Macedonia, Former Yugoslav Republic of': 'Central European Standard Time', 'Madagascar': 'E. Africa Standard Time', 'Malawi': 'South Africa Standard Time', 'Malaysia': 'Singapore Standard Time', 'Maldives': 'West Asia Standard Time', 'Mali': 'Greenwich Standard Time', 'Malta': 'W. Europe Standard Time', 'Man, Isle of': 'GMT Standard Time', 'Marshall Islands': 'UTC+12', 'Martinique': 'SA Western Standard Time', 'Mauritania': 'Greenwich Standard Time', 'Mauritius': 'Mauritius Standard Time', 'Mayotte': 'E. Africa Standard Time', 'Mexico': 'Central Standard Time (Mexico)', 'Micronesia': 'West Pacific Standard Time', 'Moldova': 'GTB Standard Time', 'Monaco': 'W. Europe Standard Time', 'Mongolia': 'Ulaanbaatar Standard Time', 'Montenegro': 'Central European Standard Time', 'Montserrat': 'SA Western Standard Time', 'Morocco': 'Morocco Standard Time', 'Mozambique': 'South Africa Standard Time', 'Myanmar': 'Myanmar Standard Time', 'Namibia': 'Namibia Standard Time', 'Nauru': 'UTC+12', 'Nepal': 'Nepal Standard Time', 'Netherlands': 'W. Europe Standard Time', 'New Caledonia': 'Central Pacific Standard Time', 'New Zealand': 'New Zealand Standard Time', 'Nicaragua': 'Central America Standard Time', 'Niger': 'W. Central Africa Standard Time', 'Nigeria': 'W. Central Africa Standard Time', 'Niue': 'UTC-11', 'Norfolk Island': 'Central Pacific Standard Time', 'North Korea': 'Korea Standard Time', 'Northern Mariana Islands': 'West Pacific Standard Time', 'Norway': 'W. Europe Standard Time', 'Oman': 'Arabian Standard Time', 'Pakistan': 'Pakistan Standard Time', 'Palau': 'Tokyo Standard Time', 'Palestinian Authority': 'Egypt Standard Time', 'Panama': 'SA Pacific Standard Time', 'Papua New Guinea': 'West Pacific Standard Time', 'Paraguay': 'Paraguay Standard Time', 'Peru': 'SA Pacific Standard Time', 'Philippines': 'Singapore Standard Time', 'Pitcairn Islands': 'Pacific Standard Time', 'Poland': 'Central European Standard Time', 'Portugal': 'GMT Standard Time', 'Puerto Rico': 'SA Western Standard Time', 'Qatar': 'Arab Standard Time', 'Reunion': 'Mauritius Standard Time', 'Romania': 'GTB Standard Time', 'Russia': 'Russian Standard Time', 'Rwanda': 'South Africa Standard Time', 'Saint Barthélemy': 'SA Western Standard Time', 'Saint Helena, Ascension and Tristan da Cunha': 'Greenwich Standard Time', 'Saint Kitts and Nevis': 'SA Western Standard Time', 'Saint Lucia': 'SA Western Standard Time', 'Saint Martin (French part)': 'SA Western Standard Time', 'Saint Pierre and Miquelon': 'Greenland Standard Time', 'Saint Vincent and the Grenadines': 'SA Western Standard Time', 'Samoa': 'Samoa Standard Time', 'San Marino': 'W. Europe Standard Time', 'São Tomé and Príncipe': 'Greenwich Standard Time', 'Saudi Arabia': 'Arab Standard Time', 'Senegal': 'Greenwich Standard Time', 'Serbia': 'Central Europe Standard Time', 'Seychelles': 'Mauritius Standard Time', 'Sierra Leone': 'Greenwich Standard Time', 'Singapore': 'Singapore Standard Time', 'Sint Maarten (Dutch part)': 'SA Western Standard Time', 'Slovakia': 'Central Europe Standard Time', 'Slovenia': 'Central Europe Standard Time', 'Solomon Islands': 'Central Pacific Standard Time', 'Somalia': 'E. Africa Standard Time', 'South Africa': 'South Africa Standard Time', 'South Georgia and the South Sandwich Islands': 'UTC-02', 'South Sudan': 'E. Africa Standard Time', 'Spain': 'Romance Standard Time', 'Sri Lanka': 'Sri Lanka Standard Time', 'Sudan': 'E. Africa Standard Time', 'Suriname': 'SA Eastern Standard Time', 'Svalbard': 'W. Europe Standard Time', 'Swaziland': 'South Africa Standard Time', 'Sweden': 'W. Europe Standard Time', 'Switzerland': 'W. Europe Standard Time', 'Syria': 'Syria Standard Time', 'Taiwan': 'Taipei Standard Time', 'Tajikistan': 'West Asia Standard Time', 'Tanzania': 'E. Africa Standard Time', 'Thailand': 'SE Asia Standard Time', 'Togo': 'Greenwich Standard Time', 'Tokelau': 'Tonga Standard Time', 'Tonga': 'Tonga Standard Time', 'Trinidad and Tobago': 'SA Western Standard Time', 'Tunisia': 'W. Central Africa Standard Time', 'Turkey': 'Turkey Standard Time', 'Turkmenistan': 'West Asia Standard Time', 'Turks and Caicos Islands': 'Eastern Standard Time', 'Tuvalu': 'UTC+12', 'U.S. Minor Outlying Islands': 'UTC-11', 'Uganda': 'E. Africa Standard Time', 'Ukraine': 'FLE Standard Time', 'United Arab Emirates': 'Arabian Standard Time', 'United Kingdom': 'GMT Standard Time', 'United States': 'Pacific Standard Time', 'Uruguay': 'Montevideo Standard Time', 'Uzbekistan': 'West Asia Standard Time', 'Vanuatu': 'Central Pacific Standard Time', 'Vatican City': 'W. Europe Standard Time', 'Vietnam': 'SE Asia Standard Time', 'Virgin Islands, U.S.': 'SA Western Standard Time', 'Virgin Islands, British': 'SA Western Standard Time', 'Wallis and Futuna': 'UTC+12', 'Yemen': 'Arab Standard Time', 'Zambia': 'South Africa Standard Time', 'Zimbabwe': 'South Africa Standard Time'}

def set_system_timezone_windows(timezone):
    try:
        subprocess.call(['tzutil', '/s', timezone])
        print("System timezone set to", timezone)
    except Exception as e:
        print("Error setting system timezone:", str(e))

# Create your views here.
def bot(keyword,ip_lst,website_name):
    ua = UserAgent()
    for i in ip_lst:
        user_agent = ua.random
        all_internal_links = []
        host, port = i.split(":")
        chrome_options = Options()
        chrome_options.add_argument('--proxy-server={0}:{1}'.format(host, port))
        chrome_options.add_argument(f"--user-agent={user_agent}")
        driver = webdriver.Chrome(executable_path='~/google_bot/impression_bot/chromedriver', options=chrome_options)
        time.sleep(30)
        try:
            driver.get('https://whatismyipaddress.com/')
        except WebDriverException as e:
            continue

        time.sleep(10)

        try:
            a = driver.find_element(By.XPATH, '//p[@class="information"][4]/span[2]')
            proxy_country = a.text
            if proxy_country in country_timezones:
                timezone = country_timezones[proxy_country]
                set_system_timezone_windows(timezone)
            else:
                proxy_country = "United States"
                if proxy_country in country_timezones:
                    timezone = country_timezones[proxy_country]
                    set_system_timezone_windows(timezone)
        except:
            proxy_country = "United States"
            timezone = country_timezones[proxy_country]
            set_system_timezone_windows(timezone)
        
        

        driver.quit()
        time.sleep(5)
        driver = webdriver.Chrome(executable_path='~/google_bot/impression_bot/chromedriver',options=chrome_options)
        time.sleep(30)
        driver.get('https://www.google.com/')

        # wait_time = int(input("Enter the time you want the bot to wait: "))
        # user_input = driver.execute_script("return prompt('Please enter your input:');")
        time.sleep(10)
        # time.sleep(5)
        try:
            driver.find_element(By.XPATH, '//textarea[@id="APjFqb"]').send_keys(keyword)
        except:
            try:
                driver.find_element(By.XPATH, '//input[@class="lst"]').send_keys(keyword)
            except:
                try:
                    driver.find_element(By.XPATH, '//input[@id="lst-ib"]').send_keys(keyword)
                except:
                    continue
        time.sleep(10)
        try:
            driver.find_element(By.XPATH, '//textarea[@id="APjFqb"]').send_keys(Keys.ENTER)
        except:
            try:
                driver.find_element(By.XPATH, '//input[@class="lst"]').send_keys(Keys.ENTER)
            except:
                driver.find_element(By.XPATH, '//input[@id="lst-ib"]').send_keys(Keys.ENTER)
        # wait_time = int(input("Enter the time you want the bot to wait: "))
        time.sleep(10)
        try:
            driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/form[2]/input[13]').click()
            time.sleep(5)
        except:
            pass
        flag = False
        while flag == False:
            try:
                if len(driver.find_elements(By.XPATH, '//div[@class="MjjYud"]//div[@class="Z26q7c UK95Uc jGGQ5e"]//a')) > 0:
                    links = driver.find_elements(By.XPATH, '//div[@class="MjjYud"]//div[@class="Z26q7c UK95Uc jGGQ5e"]//a')
                elif len(driver.find_elements(By.XPATH, '//a[@class="fuLhoc ZWRArf"]')) > 0:
                    links = driver.find_elements(By.XPATH, '//a[@class="fuLhoc ZWRArf"]')
                else:
                    links = driver.find_elements(By.XPATH, '//div[@class="egMi0 kCrYT"]/a')


            except Exception as e:
                break

            time.sleep(10)
            for link in links:
                if website_name in link.get_attribute('href'):
                    driver.get(link.get_attribute('href'))
                    time.sleep(10)
                    linkss = driver.find_elements(By.TAG_NAME, 'a')
                    for i in linkss:
                        href = i.get_attribute('href')
                        if "https://{}.com".format(website_name) in href:
                            if '#' not in href:
                                all_internal_links.append(href)
                    
                    random.shuffle(all_internal_links)

                    for i in range(3):
                        driver.get(all_internal_links[i])
                        for i in range(5):
                            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
                            time.sleep(2)
                    all_internal_links.clear()
                    flag = True
                    break
                else:
                    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
                    time.sleep(2)
                    continue

            try:
                try:
                    driver.find_element(By.XPATH, '//div[@class="GNJvt ipz2Oe"]').click()
                except:
                    driver.find_element(By.XPATH, '//a[@class="nBDE1b G5eFlf"]')
                    if driver.current_url == next_page.get_attribute('href'):
                        flag == True
                        break
                    else:
                        next_page.click()
                        time.sleep(5)
            except:
                try:
                    driver.find_element(By.XPATH, '//span[@class="RVQdVd"]').click()
                except:
                    try:
                        next_page = driver.find_element(By.XPATH, '//td[@class="d6cvqb BBwThe"][2]/a')
                        next_page.click()
                        time.sleep(5)
                    except:
                        try:
                            next_page = driver.find_element(By.XPATH, '//a[@class="nBDE1b G5eFlf"][2]')
                            if driver.current_url == next_page.get_attribute('href'):
                                flag == True
                                break
                            else:
                                next_page.click()
                                time.sleep(5)
                        except:
                            try:
                                try:
                                    next_page = driver.find_element(By.XPATH, '//td[4]//a[@class="frGj1b"]')
                                    if driver.current_url == next_page.get_attribute('href'):
                                        flag == True
                                        break
                                    else:
                                        next_page.click()
                                        time.sleep(5)
                                except:
                                    try:
                                        next_page = driver.find_element(By.XPATH, '//a[@class="frGj1b"]')
                                        if driver.current_url == next_page.get_attribute('href'):
                                            flag == True
                                            break
                                        else:
                                            next_page.click()
                                            time.sleep(5)
                                    except:
                                        next_page = driver.find_element(By.XPATH, '//a[@class="nBDE1b"]')
                                        if driver.current_url == next_page.get_attribute('href'):
                                            flag == True
                                            break
                                        else:
                                            next_page.click()
                                            time.sleep(5)
                            except:
                                flag = True
                                proxy_country = 'Pakistan'
                                if proxy_country in country_timezones:
                                    # Retrieve the corresponding timezone
                                    timezone = country_timezones[proxy_country]
                                    # Set the system timezone
                                    set_system_timezone_windows(timezone)
                                else:
                                    print("Proxy country mapping not found.")
                                driver.quit()
                                continue

            if flag == True:
                proxy_country = 'Pakistan'
                if proxy_country in country_timezones:
                    timezone = country_timezones[proxy_country]
                    set_system_timezone_windows(timezone)
                else:
                    print("Proxy country mapping not found.")
                driver.quit()
                continue
        




def start_bot(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        ip_file = request.FILES['ip_file']
        ip_lst = ip_file.read().decode().splitlines()
        website_name = request.POST.get('web_name')
        
        bot(keyword,ip_lst, website_name)
        
    return render(request, 'bot/index.html')
