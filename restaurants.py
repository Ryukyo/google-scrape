from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv

s = Service('./chromedriver')
o = Options()
o.headless = True
main_url = "https://restaurant.ikyu.com/"
# without headless option if detected as bot , options=o
browser = webdriver.Chrome(service=s, options=o)

urls = []
names = []
genres = []
prices = []
addresses = []
stations = []
phones = []

# 194 + 1
for iteration in range(1, 3):
    url_counting = (
        f"https://restaurant.ikyu.com/search?pups=2&pthm=19%3A00&xpge={iteration}&rac1=08004&pndt=1&ptaround=0&xsrt=gourmet")

    browser.get(url_counting)
    restaurant_elements = browser.find_elements(By.CLASS_NAME,
                                                'cover_3Ae77')

    for elem in restaurant_elements:
        url = elem.get_attribute("href")
        if url != None:
            urls.append(url)

for restaurant in urls:
    name = price = genre = address = phone = station = ''
    browser.get(restaurant)
    time.sleep(1)
    try:
        name_exists = browser.find_elements(By.CLASS_NAME,
                                            "restaurantName_dvSu5")
        if (name_exists):
            name = browser.find_element(By.CLASS_NAME,
                                        "restaurantName_dvSu5").get_attribute('innerText')
        price_exists = browser.find_elements(By.XPATH,
                                             "//*[@aria-label='05']/span[2]")
        if(price_exists):
            price = browser.find_element(By.XPATH,
                                         "//*[@aria-label='05']/span[2]").get_attribute('innerText')
        genre = browser.find_element(By.XPATH,
                                     "//*[@id='__layout']/div/div[2]/main/header/div/div[1]/div[1]/div/span/span").get_attribute('innerText')
        phone_exists = browser.find_elements(
            By.XPATH, "//h3[contains(text(), 'お問い合わせ')]")
        if (phone_exists):
            phone = browser.find_element(
                By.XPATH, "//h3[contains(text(), 'お問い合わせ')]/following-sibling::div").get_attribute('innerText').split('\n')[0]
            station_list = browser.find_elements(
                By.XPATH, "//h3[contains(text(), '最寄り駅')]")
            if(station_list):
                station = browser.find_element(
                    By.XPATH, "//h3[contains(text(), '最寄り駅')]/following-sibling::div").get_attribute('innerText').replace(
                    '\u3000', ' ').replace('\n', ' ')
            address = browser.find_element(
                By.XPATH, "//*[@aria-label='address']/following-sibling::div").get_attribute('innerText').replace(
                    '\u3000', ' ').replace('\n', ' ')
        else:
            station_list = browser.find_elements(
                By.XPATH, "//h3[contains(text(), '最寄り駅')]")
            if(station_list):
                station = browser.find_element(
                    By.XPATH, "//h3[contains(text(), '最寄り駅')]/following-sibling::div").get_attribute('innerText').replace(
                    '\u3000', ' ').replace('\n', ' ')
            address = browser.find_element(
                By.XPATH, "//*[@aria-label='address']/following-sibling::div").get_attribute('innerText').replace(
                    '\u3000', ' ').replace('\n', ' ')
    except NoSuchElementException as e:
        print("Exception:", e)
        continue
    finally:
        names.append(name)
        prices.append(price)
        genres.append(genre)
        addresses.append(address)
        phones.append(phone)
        stations.append(station)


combined_lists = [list(a) for a in zip(
    names, urls, prices, genres, addresses, phones, stations)]

with open('out/restaurants_hiroshima_rankings_01-23.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile, delimiter=',')
    headers = ['Venue Name', 'Venue URL', 'Price Range',
               'Genre', 'Address', 'Phone Number', 'Nearest Station']
    my_writer.writerow(i for i in headers)
    for j in combined_lists:
        my_writer.writerow(j)

browser.quit()
