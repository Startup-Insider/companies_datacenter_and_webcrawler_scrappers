import requests
from bs4 import BeautifulSoup
import csv
import re
import math
import time
import sys

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}


def page_number(html):
    soup = BeautifulSoup(html, 'html.parser')
    total_pages_raw = re.search(r'<span class="red">(\d+)</span>', html)

    total_results = 0
    if total_pages_raw:
        total_results = int(total_pages_raw.group(1))
    else:
        print("TOTAL PAGES NOT FOUND")
        return " of N/A"

    for delete_hidden in soup.select('div.startup-cards > div.d-xl-none.d-flex'):
        delete_hidden.decompose()

    startup_box = soup.select('div.startup-cards > div.white-box.startup-box')

    item_per_page = len(startup_box)

    total_pages = math.ceil(total_results / item_per_page)

    print(f'\nTotal Results:   {total_results}')
    print(f'Items per page:  {item_per_page}')
    print(f'Total pages:     {total_pages}\n\n')

    return f' of {total_pages}'


def parse_item_page(url):
    global headers
    print(f'Requesting https://www.startup.ch{url}')

    # file_name = url.replace('/', '')
    response_item = requests.get(f'https://www.startup.ch{url}', headers=headers)
    # with open(f'startupch/{file_name}.html', 'w', encoding='utf-8') as file:
    #     file.write(response_item.text)
    response_item_text = response_item.text

    # with open(f'startupch/skinmind.html', 'r', encoding='utf-8') as file:
    #     response_item_text = file.read()

    soup_item = BeautifulSoup(response_item_text, 'html.parser')

    to_return = {
        'name': "N/A",
        'shot_description': "N/A",
        'website': "N/A",
        'headquarter': "N/A",
        'founded': "N/A",
        'main_sector': "N/A",
    }

    to_return['name'] = soup_item.select_one('h1').text.strip()

    to_return['shot_description'] = soup_item.select_one('h5').text.strip()

    website_raw = soup_item.select_one('p.startup-webpage-link > a')

    if website_raw:
        to_return['website'] = website_raw.get('href')

    headquarter_raw = soup_item.select_one('p.headquarters')

    if headquarter_raw:
        to_return['headquarter'] = (headquarter_raw.text.strip().replace('Headquarter:', '')
                                    .replace('\r\n', '')
                                    .replace('\r', '')
                                    .replace('\n', '')
                                    .replace('\t', ''))

    founded_raw = soup_item.select_one('p.foundation-date')

    if founded_raw:
        to_return['founded'] = (founded_raw.text.strip().replace('Foundation Date:', '')
                                .replace('\r\n', '')
                                .replace('\r', '')
                                .replace('\n', '')
                                .replace('\t', ''))

    sectors_raw = soup_item.select('div.sectors.w-100 >ul>li')

    if len(sectors_raw) > 0:
        to_return['main_sector'] = sectors_raw[0].text

    if len(sectors_raw) > 1:
        to_return['sectors'] = ",".join([d.text for d in sectors_raw[1:]])

    return to_return


def parse_cat(html):
    soup = BeautifulSoup(html, 'html.parser')

    for delete_hidden in soup.select('div.startup-cards > div.d-xl-none.d-flex'):
        delete_hidden.decompose()

    startup_box = soup.select('div.startup-cards > div.white-box.startup-box')

    to_csv=[]
    for sb in startup_box:
        link = sb.select_one('a')
        if not link:
            continue
        csv_data = parse_item_page(link.get('href'))
        to_csv.append(list(csv_data.values()))

    with open('csv/startupch.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)

    pagination = soup.select('ul.pagination.justify-content-center > li.page-item')
    next_page_link = None

    if pagination:
        last_page_item = pagination[-1]
        next_page = last_page_item.select_one('a')

        if next_page:
            next_page_link = next_page.get('href')

        else:
            print("SCRAPING END")

    else:
        print("PAGINATION_ERROR")
    return next_page_link


# -------------------------------------------- functions end ------------------------------


with open('csv/startupch.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "shot description","website","headquarter","founded","main_sector","sectors"])

response = requests.get('https://www.startup.ch/startup-directory', headers=headers)
total_pages = page_number(response.text)
next_page = parse_cat(response.text)

print(f"-------------- end page: 1{total_pages}\n")
count_page = 2

while True:
    response = requests.get(f'https://www.startup.ch{next_page}', headers=headers)
    next_page = parse_cat(response.text)

    if next_page is None:
        break

    print(f"-------------- end page: {count_page}{total_pages}\n")
    count_page += 1