from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import csv

url = "https://www.private-bildung.com/privatschulen/baden-wuerttemberg/"
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)

urls = []
mails = []
names = []

for iteration in range(1, 63):
    url_counting = (
        f"https://www.private-bildung.com/privatschulen/baden-wuerttemberg/0-0-0-0-0-0-0-0/{iteration}")

    driver.get(url_counting)
    school_elements = driver.find_elements_by_class_name(
        'content-box-shadow')

    for elem in school_elements:
        url = elem.get_attribute("href")
        if url != None:
            urls.append(url)

for school in urls:
    driver.get(school)
    try:
        name = driver.find_element_by_xpath(
            "//h3[@itemprop='name']").get_attribute('innerText')
        mail = driver.find_element_by_xpath(
            "//span[@itemprop='email']").get_attribute('innerText')
        mails.append(mail)
        names.append(name)
    except NoSuchElementException:
        continue

# print(mails, names)

combined_lists = [list(a) for a in zip(names, mails)]

driver.quit()

with open('out/privatschulen_bw.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(combined_lists)
