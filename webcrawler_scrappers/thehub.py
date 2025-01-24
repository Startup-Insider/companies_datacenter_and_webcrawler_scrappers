import requests
import json
import csv

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://thehub.io/startups',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

with open('csv/thehub.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["name","website","numberOfEmployees","founded","industries","whatWeDo"])

page =1
while True:
    response = requests.get(f'https://thehub.io/api/companies?page={page}', headers=headers)
    try:
        rows = response.json()
    except:
        print(f"error json decode {response.text}")
        break
    print(f"page {page} of {rows['pages']}")
    to_csv = []
    for row in rows['docs']:
        industries = ",".join(row['industries'])
        to_csv.append([row['name'], row['website'], row['numberOfEmployees'], row['founded'],industries,
                       row['whatWeDo'].replace("\r\n","").replace("\n","")])

    with open('csv/thehub.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)
    page += 1
    if page >= rows['pages']:
        break
