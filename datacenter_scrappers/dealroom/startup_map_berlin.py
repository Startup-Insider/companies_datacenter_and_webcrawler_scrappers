from curl_cffi import requests
import json
import time
import csv
import sys
from dealroom_module import DealRoomJsonHandler

proxy_data = 'http://username:password@host:port'
parser = DealRoomJsonHandler('start_map_berlin.csv')


#---------------------------------------------------------------------------------------

def items_on_page(data, first_loop=False):
    global parser
    parser.main_function(data, first_loop)


#---------------------------------------------------------------------------------------
def api_request(offset):
    global proxy_data
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://startup-map.berlin',
        'priority': 'u=1, i',
        'referer': 'https://startup-map.berlin/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-dealroom-app-id': '110618058',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'fields': 'uuid,website_url,appstore_app_id,client_focus,company_status,corporate_industries,employees_chart,employees_latest,'
                  'employees,entity_sub_types,employee_12_months_growth_percentile,employee_12_months_growth_unique,similarweb_12_months_growth_percentile,'
                  'similarweb_12_months_growth_unique,similarweb_12_months_growth_delta,similarweb_12_months_growth_relative,similarweb_3_months_growth_delta,'
                  'similarweb_3_months_growth_percentile,similarweb_3_months_growth_relative,similarweb_3_months_growth_unique,similarweb_6_months_growth_delta,'
                  'similarweb_6_months_growth_percentile,similarweb_6_months_growth_relative,similarweb_6_months_growth_unique,facebook_url,founders,growth_stage,'
                  'hq_locations,income_streams,industries,innovations_count,investments,investors,is_editorial,kpi_summary,latest_valuation_enhanced,'
                  'launch_month,launch_year,linkedin_url,lists_ids,lists,name,patents_count,path,playmarket_app_id,revenues,sdgs,service_industries,similarweb_chart,'
                  'sub_industries,tags,tagline,technologies,total_funding_enhanced,type,tech_stack,twitter_url,employee_12_months_growth_delta,'
                  'employee_12_months_growth_relative,employee_3_months_growth_delta,employee_3_months_growth_percentile,employee_3_months_growth_relative,'
                  'employee_3_months_growth_unique,employee_6_months_growth_delta,employee_6_months_growth_percentile,employee_6_months_growth_relative,'
                  'employee_6_months_growth_unique,founders_score_cumulated,founders,founders_top_university,founders_top_past_companies,fundings,has_strong_founder,'
                  'has_super_founder,images,innovations,innovation_corporate_rank,is_ai_data,ipo_round,latest_revenue_enhanced,matching_score,past_founders_raised_10m,'
                  'past_founders,startup_ranking_rating,total_jobs_available,year_became_unicorn,year_became_future_unicorn,job_roles',
        'limit': 25,
        f'offset': offset,
        'form_data': {
            'must': {
                'filters': {
                    'all_regions': {
                        'values': [
                            'Berlin/Brandenburg Metropolitan Region',
                        ],
                        'execution': 'or',
                    },
                    'data_type': {
                        'values': [
                            'Verified',
                        ],
                        'execution': 'or',
                    },
                },
                'execution': 'and',
            },
            'should': {
                'filters': {},
            },
            'must_not': {
                'growth_stages': [
                    'mature',
                ],
                'company_type': [
                    'service provider',
                    'government nonprofit',
                ],
                'tags': [
                    'outside tech',
                ],
                'company_status': [
                    'closed',
                ],
            },
        },
        'multi_match': False,
        'keyword_match_type': 'fuzzy',
        'sort': 'startup_ranking_runners_up_rank',
        'keyword_type': 'default_next',
    }

    proxies = {
        'http': proxy_data,
        'https': proxy_data
    }

    # response_proxy = requests.post('https://ipv4.icanhazip.com/', proxies=proxies)
    # print("Proxy>>>",response_proxy.text)

    response = requests.post('https://api.dealroom.co/api/v2/companies',
                             # proxies=proxies,
                             impersonate="chrome101",
                             headers=headers, json=json_data)
    # print(response.text)

    print("response: ", response)

    data = response.json()
    return data


#---------------------------------------------------------------------------------------


data = api_request(0)

# print(data)
try:
    total_companies = data['total']
except:
    print(data)
    print("IP BANNED!!")
    sys.exit(0)

print(f'TOTAL COMPANIES {total_companies}')
items_on_page(data, True)
print(f'-----------------------------DONE 25/{total_companies}')

for i in range(25, total_companies, 25):
    data = api_request(i)
    items_on_page(data)
    print(f'-----------------------------DONE {i+25}/{total_companies}')
    time.sleep(1.5)
    # break
