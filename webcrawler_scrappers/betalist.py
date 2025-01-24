import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'accept': 'text/html, application/xhtml+xml',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'if-none-match': 'W/"45a6dd2ed037d200dc85eeee3b67c98b"',
    'priority': 'u=1, i',
    'referer': 'https://betalist.com/regions/europe',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'turbo-frame': 'pagination',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

stop_signal = False


def request_item_page(item_url):
    global headers
    print(f'REQUESTING https://betalist.com{item_url}')
    response_item = requests.get(f'https://betalist.com{item_url}', headers=headers)
    soup2 = BeautifulSoup(response_item.text, 'html.parser')
    website_raw = soup2.select_one('a.bg-black.text-white.text-lg.font-medium.rounded.px-4.py-3')

    to_return = "no_data"
    if website_raw:
        website302 = website_raw.get('href')
        response_redirect = requests.get(f'https://betalist.com{website302}', allow_redirects=False)

        if response_redirect.status_code == 302:
            to_return = response_redirect.headers.get('Location').split("?ref=")[0]

    return to_return


def scrape_cat(response_raw):
    global stop_signal
    response = response_raw.replace('template>', 'template2>')  #!!! do not delete this line its a bs4 bug hack !!!
    soup = BeautifulSoup(response, 'html.parser')
    items = soup.select('template2 > div.block')

    if len(items) < 10:
        stop_signal = True

    to_csv = []

    for item in items:
        link_raw = item.select_one('a.block.whitespace-nowrap.text-ellipsis.overflow-hidden.font-medium')
        try:
            name = link_raw.text.strip()
            shot_description = item.select_one('a.block.text-gray-500').text.strip()
            inner_url = link_raw.get('href')

        except:
            name = shot_description = inner_url = "no_data"

        # print(name, "|", shot_description, "|", 'https://betalist.com' + inner_url)

        website = request_item_page(inner_url)
        to_csv.append([name, shot_description, website])

    with open('csv/betalist.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)


#----------------------------------------func end

with open('csv/betalist.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "shot description","website"])

page = 1
while True:
    if stop_signal:
        print("END SCRAPING")
        break
    response = requests.get(f'https://betalist.com/regions/europe.turbo_stream?page={page}', headers=headers)
    scrape_cat(response.text)
    print(f'end page {page}\n')
    page += 1

