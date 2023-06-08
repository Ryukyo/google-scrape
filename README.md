# google-scrape

Scrape Google search results into CSV file (using the main.py file)\
Or scrape data directly from websites (all other python scripts)

## Setup

1. `virtualenv -p python3.10 venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

For scripts using Selenium, a version of Chromedriver matching your Chrome Browser version is required

## Run

### Using beautiful soup and the main.py file for Google results

1. Enter search terms in queries.txt
2. Run `python3 main.py` in your terminal

Go to `http://127.0.0.1:8000` in browser

### Using Selenium on other websites

1. Run `python3 'name_of_script'.py` in your terminal
