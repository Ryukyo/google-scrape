from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv

s = Service('./chromedriver')
options = Options()
options.headless = True
main_url = "https://tabelog.com/"
# without headless option if detected as bot , options=options
browser = webdriver.Chrome(service=s, options=options)

urls = []
names = []
genres = []
prices = []
addresses = []
stations = []
phones = []

# 194 + 1
for iteration in range(1, 53):
    url_counting = (
        f"https://tabelog.com/saitama/rstLst/{iteration}/?LstSmoking=0&svd=20230104&svt=1900&svps=2&LstCos=5&RdoCosTp=2")

    browser.get(url_counting)
    restaurant_elements = browser.find_elements(By.XPATH,
                                                "//*[@class='list-rst__rst-name-target cpy-rst-name']")

    for elem in restaurant_elements:
        url = elem.get_attribute("href")
        if url != None:
            urls.append(url)

for restaurant in urls:
    name = price = genre = address = phone = station = ''
    browser.get(restaurant)
    time.sleep(2)
    try:
        name = browser.find_element(By.CLASS_NAME,
                                    "rstinfo-table__name-wrap").get_attribute('innerText').replace('\n', ' ')
        price_exists = browser.find_elements(By.XPATH,
                                             "//*[@id='rst-data-head']/table[1]/tbody/tr[8]/td/div")
        if(price_exists):
            price = browser.find_element(By.CLASS_NAME,
                                         "rstinfo-table__budget-item").get_attribute('innerText')
        genre = browser.find_element(By.XPATH,
                                     "//*[@id='rst-data-head']/table[1]/tbody/tr[2]/td/span").get_attribute('innerText')
        phone_exists = browser.find_elements(
            By.CLASS_NAME, "rstinfo-table__tel-num")
        if (phone_exists):
            phone = browser.find_element(
                By.CLASS_NAME, "rstinfo-table__tel-num").get_attribute('innerText')
        station_list = browser.find_elements(
            By.XPATH, "//*[@id='rst-data-head']/table[1]/tbody/tr[6]/td/p[1]")
        if(station_list):
            station = browser.find_element(
                By.XPATH, "//*[@id='rst-data-head']/table[1]/tbody/tr[6]/td/p[1]").get_attribute('innerText')
        address = browser.find_element(
            By.CLASS_NAME, "rstinfo-table__address").get_attribute('innerText')
    except NoSuchElementException as e:
        print("Exception:", e)
        # continue
    finally:
        names.append(name)
        prices.append(price)
        genres.append(genre)
        addresses.append(address)
        phones.append(phone)
        stations.append(station)


combined_lists = [list(a) for a in zip(
    names, urls, prices, genres, addresses, phones, stations)]

with open('out/tabelog/restaurants_saitama_01-23.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile, delimiter=',')
    headers = ['Venue Name', 'Venue URL', 'Price Range',
               'Genre', 'Address', 'Phone Number', 'Nearest Station']
    my_writer.writerow(i for i in headers)
    for j in combined_lists:
        my_writer.writerow(j)

browser.quit()
