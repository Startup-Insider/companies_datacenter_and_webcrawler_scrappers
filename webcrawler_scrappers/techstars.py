import requests
import csv
import math
import time

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'origin': 'https://www.techstars.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'x-typesense-api-key': 'rGlcUJRbfJofJrynCngiBoMZturrg1Of',
}

with open('csv/techstars.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["company_name", "state_province", "website", "worldregion", "worldsubregion", "practice_area",
                     "program_names", "brief_description"])

page = 1

while True:
    response_str = requests.get(
        f'https://websearch.techstars.com/collections/companies/documents/search?page={page}&per_page=250&q=&query_by=company_name,brief_description,practice_area,city,state_province,country,worldregion,program_names&sort_by=website_order:asc&filter_by=&facet_by=is_bcorp,is_1b,is_current_session,practice_area,worldregion,is_exit,first_session_year,program_names&max_facet_values=100',
        headers=headers,
    )
    response = response_str.json()
    to_csv = []
    for row_long in response['hits']:
        row = row_long['document']
        if 'practice_area' in row:
            practice_area = ",".join(row['practice_area'])
        else:
            practice_area = 'no_data'

        if 'program_names' in row:
            program_names = "|".join(row['program_names'])
        else:
            program_names = 'no_data'

        if 'state_province' in row:
            state_province = row['state_province']
        else:
            state_province = 'no_data'

        if 'brief_description' in row:
            brief_description = row['brief_description']
        else:
            brief_description = 'no_data'

        if 'worldregion' in row:
            worldregion = row['worldregion']
        else:
            worldregion = 'no_data'

        if 'worldsubregion' in row:
            worldsubregion = row['worldsubregion']
        else:
            worldsubregion = 'no_data'

        if 'website' in row:
            website = row['website']
        else:
            website = 'no_data'

        to_csv.append([row['company_name'], state_province, website,
                       worldregion, worldsubregion, practice_area, program_names,
                       brief_description])

    with open('csv/techstars.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)
    pages = math.ceil(response['out_of'] / 250)
    print(f'Total: {response["out_of"]} current page {response["page"]} of {pages}')
    page += 1
    if response['page'] >= pages:
        break
    time.sleep(0.5)
