from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import csv

url = "https://www.saarland.de/mbk/DE/portale/bildungsserver/themen/schulen-und-bildungswege/schuldatenbank/_functions/Schulsuche_Formular.html?submit=Suchen&sortOrder=schule_sort%20asc"
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)

school_elements = driver.find_elements_by_class_name(
    'c-teaser-card')
urls = []
mails = []
names = []


for elem in school_elements:
    # print(elem.get_attribute('innerHTML'))
    try:
        # print(elem)
        name = elem.find_element_by_tag_name('h3').get_attribute('innerText')
        mail = elem.find_element_by_css_selector(
            "[title^='E-Mail']").get_attribute('innerText')
        mails.append(mail)
        names.append(name)
    except NoSuchElementException:
        continue

for iteration in range(2, 35):
    url_counting = (
        f"https://www.saarland.de/mbk/DE/portale/bildungsserver/themen/schulen-und-bildungswege/schuldatenbank/_functions/Schulsuche_Formular.html?gtp=%2526c5706df2-b646-40cc-8c62-b7a95b0cb40e_list%253D{iteration}&submit=Suchen&sortOrder=schule_sort%20asc")
    # print(url_counting)
    driver.get(url_counting)
    school_elements = driver.find_elements_by_class_name(
        'c-teaser-card')

    for elem in school_elements:
        try:
            name = elem.find_element_by_tag_name(
                'h3').get_attribute('innerText')
            mail = elem.find_element_by_css_selector(
                "[title^='E-Mail']").get_attribute('innerText')
            mails.append(mail)
            names.append(name)
        except NoSuchElementException:
            continue


combined_lists = [list(a) for a in zip(names, mails)]

driver.quit()

with open('out/schulen_saarland.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(combined_lists)
