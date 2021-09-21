from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import csv

url = "https://www.bildung.berlin.de/Schulverzeichnis/SchulListe.aspx"
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)

time.sleep(5)

a_elements = driver.find_elements_by_xpath(
    "//table[@id='DataListSchulen']//a")
urls = []
mails = []
names = []

for elem in a_elements:
    url = elem.get_attribute("href")
    urls.append(url)

for elem in urls:
    driver.get(elem)
    try:
        name = driver.find_element_by_id(
            'ContentPlaceHolderMenuListe_lblSchulname').get_attribute('innerText')
        mail = driver.find_element_by_id(
            'ContentPlaceHolderMenuListe_HLinkEMail').get_attribute('innerText')
        mails.append(mail)
        names.append(name)
    except NoSuchElementException:
        continue

# print(mails, names)


combined_lists = [list(a) for a in zip(names, mails)]

driver.quit()

with open('out/schulen_berlin.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(combined_lists)
