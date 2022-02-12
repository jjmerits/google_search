
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from bs4.element import Tag
import subprocess
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

headers  = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36")
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
google_url = "https://www.google.com/search?q=teladoc acquisition" + "&num=" + str(100)
driver.get(google_url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source,'lxml')
result_div = soup.find_all('div', attrs={'id': 'rso'})


links = []
titles = []
descriptions = []
for r in result_div:
    # Checks if each element is present, else, raise exception
    try:
        link = r.find('a', href=True)
        title = None
        title = r.find('h3')

        if isinstance(title,Tag):
            title = title.get_text()

        description = None
        description = r.select('div > div:nth-child(2) > div > span:nth-child(2)')[0]

        if isinstance(description, Tag):
            description = description.get_text()

        # Check to make sure everything is present before appending
        if link != '' and title != '' and description != '':
            links.append(link['href'])
            titles.append(title)
            descriptions.append(description)
    # Next loop if one element is not present
    except Exception as e:
        print(e)
        continue

print(titles)
print(links)
print(descriptions)

import urllib.request
render(request, 'data.html', result_div[0])