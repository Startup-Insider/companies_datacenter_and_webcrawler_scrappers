import requests
from bs4 import BeautifulSoup
import csv

num_pages = 10


def scrape(response, page):
    soup = BeautifulSoup(response, 'html.parser')
    if page < 3:
        global num_pages
        num_pages = int(soup.select_one('div.container.my-default.d-none.d-no-js-block').text.split('of')[1].strip())

    to_csv = []
    items = soup.select('ul#startups-list-results >li')

    for item in items:
        name = item.select_one('h2').text.strip()
        description = item.select_one('p').text.strip().replace('\r\n', '').replace('\n', '')
        try:
            site = item.select_one('a.meta-item.fw-bold.stretched-link').get('href')
        except:
            site = 'none'

        add_data = item.select('span.meta-item')
        category = category2 = 'none'
        if len(add_data) > 0:
            country = add_data[0].text.strip()
        if len(add_data) > 1:
            category = add_data[1].text.strip()
        if len(add_data) > 2:
            category2 = add_data[2].text.strip()
        to_csv.append([name, site, category, category2, country, description])

    with open('csv/ai_startups_europe.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)
    return num_pages


headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'if-modified-since': 'Sun, 15 Sep 2024 12:19:36 GMT',
    'if-none-match': '"6ac8e-62227783ada72-gzip"',
    'priority': 'u=1, i',
    'referer': 'https://www.ai-startups-europe.eu/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

with open('csv/ai_startups_europe.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'site', 'category', 'category2', 'country', 'description'])

page = 1
while True:
    response = requests.get(f'https://www.ai-startups-europe.eu/p{page}', headers=headers)
    scrape(response.text, page)
    print(f"page {page} of {num_pages}")
    if page >= num_pages:
        break
    page += 1
