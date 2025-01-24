import requests
import json
import csv

headers = {
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://www.ycombinator.com',
    'Referer': 'https://www.ycombinator.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = '{"requests":[{"indexName":"YCCompany_production","params":"facetFilters=%5B%5B%22batch%3AS24%22%5D%2C%5B%22regions%3AEurope%22%5D%5D&facets=%5B%22app_answers%22%2C%22app_video_public%22%2C%22batch%22%2C%22demo_day_video_public%22%2C%22highlight_black%22%2C%22highlight_latinx%22%2C%22highlight_women%22%2C%22industries%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22question_answers%22%2C%22regions%22%2C%22subindustry%22%2C%22tags%22%2C%22top_company%22%5D&hitsPerPage=1000&maxValuesPerFacet=1000&page=0&query=&tagFilters="},{"indexName":"YCCompany_production","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22regions%3AEurope%22%5D%5D&facets=batch&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="},{"indexName":"YCCompany_production","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22batch%3AS24%22%5D%5D&facets=regions&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="}]}'

response = requests.post(
    'https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.16.1)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=MjBjYjRiMzY0NzdhZWY0NjExY2NhZjYxMGIxYjc2MTAwNWFkNTkwNTc4NjgxYjU0YzFhYTY2ZGQ5OGY5NDMxZnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMiUyQyUyMllDQ29tcGFueV9CeV9MYXVuY2hfRGF0ZV9wcm9kdWN0aW9uJTIyJTVEJnRhZ0ZpbHRlcnM9JTVCJTIyeWNkY19wdWJsaWMlMjIlNUQmYW5hbHl0aWNzVGFncz0lNUIlMjJ5Y2RjJTIyJTVE',
    headers=headers,
    data=data,
)
data = response.json()

to_csv = []
for row in data['results'][0]['hits']:
    tags = ",".join(row['tags'])
    industries = ",".join(row['industries'])
    regions = ",".join(row['regions'])

    to_csv.append([row['name'], row['website'], row['team_size'], tags, industries, regions, row['one_liner'],
                   row['long_description'].replace("\r\n", "").replace("\n", "")])

fieldnames = ["name", "website", "team_size", "tags", "industries", "regions", "one_liner", "long_description"]

with open('csv/ycombinator.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(fieldnames)
    writer.writerows(to_csv)
