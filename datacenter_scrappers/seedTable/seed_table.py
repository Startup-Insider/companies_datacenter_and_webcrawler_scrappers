from curl_cffi import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import sys
import json

csv_path = 'seedTable.csv'

work_path = '/'.join(csv_path.split('/')[:-1])
if len(work_path) > 0:
    work_path = work_path + '/'

unique_startup = set()

time_sleep = 1  #sleep before visiting profile

european_countries = [
    "UK", "Germany", "France", "Spain", "Sweden", "Switzerland", "Netherlands", "Italy",
    "Denmark", "Finland", "Norway", "Ireland", "Belgium", "Scotland", "Poland", "Portugal",
    "Estonia", "Austria", "Czech Republic", "Bulgaria", "Hungary", "Iceland", "Romania",
    "Malta", "Lithuania", "Luxembourg", "Greece", "Latvia", "Slovakia", "Slovenia"
]

headers = {
    'Referer': 'https://www.seedtable.com/startup-rankings',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

index_offset = 0


def get_startup_info(url_category):
    global csv_path, unique_startup
    to_return = []

    response = requests.get(url_category, headers=headers, impersonate="chrome101")

    if 404 == response.status_code:
        print("Category Not found")
        return
    if 200 != response.status_code:
        print(f"Server returns error code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    listing = soup.select('div.group.relative.block.h-full')
    print(len(listing), " startups found")
    count_req = 1
    for lst_iterate in listing:
        profile_url = lst_iterate.select_one('a')

        if profile_url.get('href') in unique_startup:
            print(f"      skiping {profile_url.get('href')} [already in csv]")
            count_req += 1
            continue

        result_dict = {"startup_name": "none", "shot_desc": "none", "profile_url": "none",
                       "industries": "none", "Location": "none",
                       "Founded": "none", "Seedtable Rank": "none",
                       "Employees": "none", "total raised": "none", "last funding": "none",
                       "persons": "none", "site": "none"}

        name = lst_iterate.select_one('a h2')
        result_dict["startup_name"] = name.text
        result_dict["profile_url"] = profile_url.get("href")

        other_data = lst_iterate.select_one('div.flex-grow')
        shot_desc = other_data.select_one('p.text-xs.sm\\:text-sm.mb-2')
        result_dict["shot_desc"] = shot_desc.text

        industries = ", ".join([ind.text for ind in other_data.select('div.flex.flex-wrap.gap-1.mb-2 > span')])
        result_dict["industries"] = industries

        raw_data = other_data.select('div.grid.grid-cols-2.gap-2.mb-2.text-xs >div')

        for single_div in raw_data:
            p_str = single_div.select("p")
            count = 0
            for p in p_str:
                p_text = p.text.replace(':', '')
                if p_text in result_dict:
                    try:
                        result_dict[p_text] = p_str[count + 1].text
                    except:
                        print(f'   [debug] NO {p_text} for {result_dict["startup_name"]}')
                count += 1

        raised = other_data.select('p.text-xs.mb-1')

        for r in raised:
            if "Total Raised:" in r.text:
                result_dict["total raised"] = r.text.replace("Total Raised: ", "")
            if "Last Funding:" in r.text:
                result_dict["last funding"] = r.text.replace("Last Funding: ", "")

        persons_html = other_data.select('div.mt-2 > ul > li')
        if persons_html:
            result_dict["persons"] = ", ".join([p_h.text for p_h in persons_html])
        result_dict['site'] = scrape_profile(result_dict['profile_url'], count_req)
        to_return.append(list(result_dict.values()))
        unique_startup.add(result_dict['profile_url'])
        count_req += 1
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_return)


# -------------------------------------------------func end --------------------------------------------------------
def scrape_profile(profile_url, count_req):
    global time_sleep
    time.sleep(time_sleep)
    global headers
    print(f"    {count_req} request {profile_url}")
    profile_response = requests.get(f"https://www.seedtable.com{profile_url}", headers=headers,
                                    impersonate="chrome101")

    soup2 = BeautifulSoup(profile_response.text, 'html.parser')
    site_url = soup2.select_one('a.text-blue-300.hover\\:underline.hover\\:text-white')
    if site_url:
        return site_url.get('href')
    return "none"


# -------------------------------------------------func end --------------------------------------------------------
def create_new_csv():
    global csv_path
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "startup_name", "shot_desc", "profile_url",
            "industries", "Location", "Founded", "Seedtable Rank",
            "Employees", "total raised", "last funding", "persons", "site"
        ])


# -------------------------------------------------func end --------------------------------------------------------

def create_index():
    global work_path
    result_tech = []
    result_city = []
    result_industries = []
    result_combined = []
    result_main = []

    response_cat1 = requests.get('https://www.seedtable.com/tech-industries', headers=headers, impersonate="chrome101")

    soup3 = BeautifulSoup(response_cat1.text, 'html.parser')
    sections = soup3.select('section.bg-white.dark\\:bg-gray-900')

    if len(sections) != 2:
        print("Probably HTML STRUCTURE CHANGED ")

    links = sections[0].select('a')

    europe_country = ["-uk", "-germany", "-sweden", "-france", "-spain", "-netherlands", "-switzerland"]

    count = 0
    for l in links:
        for ec in europe_country:
            if ec in l.get("href"):
                result_tech.append({'link': l.get("href")})
                count += 1
                break

    response_cat2 = requests.get('https://www.seedtable.com/startup-rankings', headers=headers, impersonate="chrome101")
    soup4 = BeautifulSoup(response_cat2.text, 'html.parser')
    sections2 = soup4.select('section.bg-white.dark\\:bg-gray-900')

    country_box = sections2[0].select(
        'div.grid.gap-6.sm\\:grid-cols-1.lg\\:grid-cols-3.lg\\:grid-rows-2.max-w-5xl.mx-auto > div')
    if not len(country_box):
        print('cant find countries boxes exit')
        sys.exit(0)

    for cb in country_box:
        country_name = cb.select_one('h1')
        if country_name.text not in european_countries:
            continue
        city_in_country = cb.select('ul.space-y-2 >li')
        for cic in city_in_country:
            a_box = cic.select_one('a')
            city_name = a_box.select_one('h3')
            result_city.append({"country": country_name.text, "city": city_name.text, "link": a_box.get('href')})

    industries_box = sections2[1].select('div.grid.lg\\:grid-cols-3.md\\:grid-cols-1.gap-1.lg\\:gap-x-8 > a')

    for ib in industries_box:
        industry_name = ib.select_one('h3')
        result_industries.append({"name": industry_name.text, "link": ib.get('href')})

    for ri in result_industries:
        url_industry = f'best-{ri["link"].replace("/", "").replace("startups-", "")}-startups-in-'
        for rc in result_city:
            url_city = rc['link'].replace('/startups-', '')
            # print(url_industry + url_city)
            result_combined.append({"link": f"/{url_industry}{url_city}"})

    result_main.extend(result_tech)
    result_main.extend(result_city)
    result_main.extend(result_industries)

    print(len(result_main), " index count without combined [city X industry]")
    result_main.extend(result_combined)

    print(len(result_main), " total index count")

    with open(f'{work_path}seedtable_index.json', 'w', encoding='utf-8') as f:
        json.dump(result_main, f, ensure_ascii=True, indent=1)


# -------------------------------------------------func end ------------------------------------------------------------
def create_index_offset():
    global work_path, index_offset
    with open(f'{work_path}seedtable_index_offset.txt', 'w') as file:
        file.write('0')
    index_offset = 0


# -------------------------------------------------func end ------------------------------------------------------------
def update_index_offset(val):
    global work_path, index_offset
    with open(f'{work_path}seedtable_index_offset.txt', 'w') as file:
        file.write(str(val))


# -------------------------------------------------func end ------------------------------------------------------------

# -------------------------------------------------start operation -----------------------------------------------------

if os.path.exists(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        saved_startups = csv.reader(csvfile)
        try:
            next(saved_startups)
        except:
            create_new_csv()
        for row in saved_startups:
            unique_startup.add(row[2])
else:
    create_new_csv()

if os.path.exists(f'{work_path}seedtable_index_offset.txt'):
    with open(f'{work_path}seedtable_index_offset.txt', 'r') as file:
        try:
            index_offset = int(file.read())
        except:
            index_offset = 0
else:
    create_index_offset()

print('index offset: ', index_offset)

if not os.path.exists(f'{work_path}seedtable_index.json'):
    create_index()
    # create_index_offset()

with open(f'{work_path}seedtable_index.json', 'r', encoding='utf-8') as f:
    index_data = json.load(f)

# -------------------------------------------------start operation end -------------------------------------------------

count_index = 0
for idt in index_data:
    count_index += 1
    if index_offset > count_index:
        continue
    print("\nCategory page: ", idt['link'])
    get_startup_info(f'https://www.seedtable.com{idt['link']}')
    update_index_offset(count_index)

# get_startup_info('https://www.seedtable.com/best-agritech-startups-in-berlin')
