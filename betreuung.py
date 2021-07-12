from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import csv

url = "https://service.salzburg.gv.at/weblist/kinderbetreuung/search"
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)
search_btn = driver.find_elements_by_id('searchSubmit')[0]
search_btn.click()
time.sleep(3)

select = Select(driver.find_element_by_css_selector(
    'select[name=searchTable_length]'))
select.select_by_visible_text('Alle')

time.sleep(3)

a_elements = driver.find_elements_by_xpath('//b/a[@href]')
urls = []
mails = []
names = []

for elem in a_elements:
    url = elem.get_attribute("href")
    urls.append(url)

for elem in urls:
    driver.get(elem)
    try:
        name = driver.find_element_by_tag_name('h3').get_attribute('innerText')
        mail = driver.find_element_by_class_name(
            'container-fluid').find_element_by_xpath('//div[position()=5]/div/a[@href]').get_attribute('innerText')
        mails.append(mail)
        names.append(name)
    except NoSuchElementException:
        continue

print(mails, names)


# filtered_names = filter(lambda x: x != '', names)
# filtered_titles = filter(lambda x: x != '', titles)
# emails = list(filtered_titles)
# schools = list(filtered_names)

# emails_cleaned = emails[3:]
# schools_shortened = schools[370:len(schools)-11]

# unwanted = {'Bildungsdirektion für Salzburg',
#             'Ländliche Hauswirtschaftsschule Klessheim',
#             'Landwirtschaftliche Fachschule Klessheim',
#             'Musikschulen des Vereins "Musikum" in Salzburg (Hauptanstalt)',
#             'Musikschulen des Vereins "Musikum" in Salzburg; Zweigstelle der Musikschule Seekirchen (503530)',
#             'Musikschulen des Vereins "Musikum" in Salzburg; Zweigstelle der Musikschule St.Johann im Pongau (504510)'}
# schools_cleaned = [ele for ele in schools_shortened if ele not in unwanted]
#

combined_lists = [list(a) for a in zip(names, mails)]

driver.quit()

with open('out/betreuung.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(combined_lists)
