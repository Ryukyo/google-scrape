from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import csv


def extract_magical_trip_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            magical_trip_url = soup.select_one("a[href*=magical-trip]")
            print(url, magical_trip_url)
            if magical_trip_url:
                return magical_trip_url["href"]
    except Exception as e:
        print(f"An error occurred while processing URL: {url}")
        print(str(e))
    return "None"


# Path to the text file containing the URLs
urls_file = "urls.txt"
# Path to the CSV file to write the results
output_file = "results.csv"
# Initialize the CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Found URL"])
# Read the list of URLs from the text file
with open(urls_file, "r") as file:
    urls = file.readlines()
# Remove leading/trailing whitespaces and newline characters
urls = [url.strip() for url in urls]
# Visit each URL and check if it contains the desired URL
for url in urls:
    found_url = None
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            found_url = extract_magical_trip_url(url)
    except Exception as e:
        print(f"An error occurred while processing URL: {url}")
        print(str(e))
    # Write the result to the CSV file
    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([url, found_url])
