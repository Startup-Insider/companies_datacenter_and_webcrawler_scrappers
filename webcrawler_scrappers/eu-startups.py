# from curl_cffi import requests
# 2833 11_per_page
import requests
from bs4 import BeautifulSoup
import sys
import csv
import time

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    # 'if-modified-since': 'Fri, 06 Sep 2024 08:57:29 GMT',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}


def pull_results(response):
    soup = BeautifulSoup(response, 'html.parser')
    listing = soup.select('div.listings.wpbdp-listings-list.list.wpbdp-grid >div.wpbdp-listing')
    print(len(listing))

    if len(listing) < 1:
        print('listing end')
        return False
    to_csv =[]
    for row in listing:
        name_proxy = row.select_one('h3 >a ')
        # name = name_proxy.text.strip()
        inner_url = name_proxy.get('href')

        key = row.find_all('span', class_='field-label')
        result = {"Business Name": "na", "Category": "na", "Based in": "na", "Tags": "na", "Founded": "na"}
        for k in key:
            val = k.find_next('div', class_='value')
            for search_key in ["Business Name", "Category", "Based in", "Tags", "Founded"]:
                if search_key == k.text:
                    result[search_key] = val.text.strip()

        result['inner_url'] = inner_url
        to_csv.append(list(result.values()))
    with open('csv/eu-startups.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)
    return True

with open('csv/eu-startups.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Business Name", "Category", "Based in", "Tags", "Founded","inner_url"])

pagination = 1
while True:
    response = requests.get(f'https://www.eu-startups.com/directory/page/{pagination}/', headers=headers)
    stop_signal = pull_results(response.text)
    if not stop_signal:
        break
    print(f'page {pagination}')
    pagination += 1
    time.sleep(1)
