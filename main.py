import datetime
import os
import pickle
import time
import re
from datetime import datetime, timedelta

now = datetime.now()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('disable-blink-features=AutomationControlled')

# Path to your webdriver
driver = webdriver.Chrome(
    service=Service(r'C:\Users\medii\.wdm\drivers\chromedriver\win32\96.0.4664.45\chromedriver.exe'), options=options)

# Necessary credentials
APARTMENTS_LINK = "https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/50670/c203l984r20+wohnung_mieten.qm_d:62,"
LOGIN_LINK = "https://www.ebay-kleinanzeigen.de/m-einloggen.html"


# If no cookies available yet
def login_and_save_cookies():
    driver.get(LOGIN_LINK)
    time.sleep(5)
    email_login = driver.find_element(By.ID, 'login-email')
    pw_login = driver.find_element(By.ID, 'login-password')
    button_login = driver.find_element(By.ID, 'login-submit')
    accept_cookie_button = driver.find_element(By.ID, 'gdpr-banner-accept')
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]

    accept_cookie_button.click()

    driver.switch_to.frame(iframe)
    captcha_button = driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')
    captcha_button.click()
    driver.switch_to.default_content()

    email_login.send_keys("EMAIL")
    pw_login.send_keys("PASSWORD")

    button_login.click()

    # # Save cookies
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def add_cookies():
    driver.get(LOGIN_LINK)
    time.sleep(5)
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)


def get_apartments():
    # Find all apartment links
    driver.get(APARTMENTS_LINK)
    time.sleep(5)
    articles = driver.find_elements(By.CSS_SELECTOR, 'a.ellipsis')
    links_on_page = []
    for item in articles:
        links_on_page.append(item.get_attribute('href'))
    print(links_on_page)


def check_for_time():
    times = []
    articles = driver.find_elements(By.CLASS_NAME, "ad-listitem.lazyload-item")
    for article in articles:
        times.append(article.find_element(By.CLASS_NAME, 'aditem-main--top--right'))

    print(articles)
    for timestamp in times:
        pattern = re.compile("^((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$)")

        if pattern.match(timestamp.text[-5:]) :
                time_text = timestamp.text
                formatted = time_text[-5:]
                formatted_time = datetime.strptime(formatted, '%H:%M')

                now_string = now.strftime('%H:%M')
                now_formatted = datetime.strptime(now_string, '%H:%M')
                # current_time = now.strptime(now,'%H:%M' )
                # formatted_current = c
                # print(current_time)
                if formatted_time.time() > (datetime.now() - timedelta(minutes=30)).time():
                    valid_entries = timestamp.parent
                    print(valid_entries)
        print(times)


if not os.path.exists('cookies.pkl'):
    login_and_save_cookies()
else:
    add_cookies()
get_apartments()
check_for_time()


