import requests
from bs4 import BeautifulSoup
import redis
import time
import threading

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def scrape_data():
    url = "https://www.nseindia.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the Nifty 50 table and extract data
    # This may need adjustment based on the website's structure
    table = soup.find('table', {'id': 'Nifty50'})
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    # Store in Redis
    r.set('nifty50_data', str(data))

def run_scraper():
    while True:
        scrape_data()
        time.sleep(300)  # Wait for 5 minutes

# Run the scraper in a separate thread
threading.Thread(target=run_scraper).start()
