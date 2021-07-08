from selenium import webdriver
import time
import csv

url = "https://www.bildung-sbg.gv.at/quicklinks/schulsuche/"
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)
search_btn = driver.find_elements_by_id('lsr_search')[0]
search_btn.click()
time.sleep(3)

a_elements = driver.find_elements_by_tag_name('a')
titles = []
names = []

for element in a_elements:
    try:
        titles.append(element.get_attribute('title'))
        names.append(element.get_attribute('innerText'))
    except Exception as e:
        print(f'No element found for {element} with error: {e}')

filtered_names = filter(lambda x: x != '', names)
filtered_titles = filter(lambda x: x != '', titles)
emails = list(filtered_titles)
schools = list(filtered_names)

emails_cleaned = emails[3:]
schools_shortened = schools[370:len(schools)-11]

unwanted = {'Bildungsdirektion für Salzburg',
            'Ländliche Hauswirtschaftsschule Klessheim',
            'Landwirtschaftliche Fachschule Klessheim',
            'Musikschulen des Vereins "Musikum" in Salzburg (Hauptanstalt)',
            'Musikschulen des Vereins "Musikum" in Salzburg; Zweigstelle der Musikschule Seekirchen (503530)',
            'Musikschulen des Vereins "Musikum" in Salzburg; Zweigstelle der Musikschule St.Johann im Pongau (504510)'}
schools_cleaned = [ele for ele in schools_shortened if ele not in unwanted]
emails_at = []

for email in emails_cleaned:
    new_string = email.replace('[at]', '@')
    emails_at.append(new_string)

combined_lists = [list(a) for a in zip(schools_cleaned, emails_at)]

driver.quit()

with open('out/schools.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(combined_lists)
