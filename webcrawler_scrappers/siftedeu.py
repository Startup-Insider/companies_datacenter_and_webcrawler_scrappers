from curl_cffi import requests
from bs4 import BeautifulSoup
import sys
import csv
import time
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}


def parse_start_page():
    global headers
    response = requests.get('https://sifted.eu/scout', headers=headers, impersonate="chrome")
    response_text = response.text
    soup = BeautifulSoup(response_text, 'html.parser')
    category_links_raw = soup.select('ul[aria-label="Scout List"] > li > a')
    to_return = [cl.get('href') for cl in category_links_raw]

    print(f'REQUESTING https://sifted.eu/scout found {len(to_return)} categories')
    return to_return


def parse_startup(url):
    global headers
    response = requests.get(f'https://sifted.eu{url}', headers=headers, impersonate="chrome")
    response_text = response.text
    # with open(f'htmls/siftedeu.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    # with open(f'htmls/siftedeu.html', 'r', encoding='utf-8') as file:
    #     response_text = file.read()
    soup = BeautifulSoup(response_text, 'html.parser')
    string_data = soup.find('script', {'id': '__NEXT_DATA__'})
    if not string_data:
        print("nodata found")
        return False

    startups_data = json.loads(string_data.string)

    data = startups_data['props']['pageProps']['dato']['list']
    print(f'Category -> https://sifted.eu{url} found {len(data)} startups')

    to_csv = []

    for single_startup in data:
        to_csv.append([single_startup['companyName'],
                       single_startup['website'],
                       single_startup['totalFunding'],
                       single_startup['location'],
                       single_startup['foundedYear'],
                       single_startup['tags'],
                       single_startup['description']
                       ])

    with open('csv/siftedeu.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)
# -------------------------------------------- functions end ------------------------------



with open('csv/siftedeu1.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["companyName", "website", "totalFunding", "location", "foundedYear", "tags", "description"])

start_page_links = parse_start_page()

for spl in start_page_links:
    parse_startup(spl)
