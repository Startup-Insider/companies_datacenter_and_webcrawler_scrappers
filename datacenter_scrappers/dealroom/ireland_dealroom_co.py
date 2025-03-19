from curl_cffi import requests
import json
import time
import csv
import sys

proxy_data = 'http://username:password@host:port'
def get_single_company(company_id):
    global proxy_data
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://ireland.dealroom.co',
        'priority': 'u=1, i',
        'referer': 'https://ireland.dealroom.co',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-dealroom-app-id': '060623092',
        'x-requested-with': 'XMLHttpRequest',
    }

    proxies = {
        'http': proxy_data,
        'https': proxy_data
    }


    response = requests.get(
        f'https://api.dealroom.co/api/v2/entities/{company_id}?fields=about,about_ai_generated,affiliated_funds,appstore_app_id,can_edit,career_page_url,client_focus,closing_month,closing_year,company_status,corporate_industries,country_experience,current_and_prev_year_fundings_num,delivery_method,employees_chart,employees_latest,employee_12_months_growth_percentile,employee_12_months_growth_unique,similarweb_12_months_growth_percentile,similarweb_12_months_growth_unique,employees,entity_sub_types,exits_higher_800m,facebook_url,fundings_investor,growth_stage,hq_locations,uuid,images(100x100),income_streams,industries,industry_experience,innovations_count,investments_higher_800m,investments_num,investments,investor_exits_funding_enhanced,investor_exits_num,investor_total_rank,investor_total,investors,is_ai_data,is_editorial,is_government,is_non_profit,is_from_traderegister,job_offers_total,kpi_summary,landscapes,latest_valuation_enhanced,launch_month,launch_year,legal_entities,linkedin_url,lists_ids,lists,lp_investments,lp_investors,name,ownerships,patents_count,path,playmarket_app_id,revenues,rounds_experience,sdgs,service_industries,share_ticker_symbol,similarweb_chart,similarweb_hidden,sub_industries,tagline,tags,team_total,tech_stack,technologies,total_funding_enhanced,traffic(top_countries,visitors,sources),twitter_url,instagram_handle,type,website_url&limit=25&offset=0',
        headers=headers,
        # proxies=proxies,
        impersonate="chrome101",
    )
    single_data = response.json()

    print(f'requesting {company_id}')
    return single_data['website_url']


#---------------------------------------------------------------------------------------

def items_on_page(data):
    to_csv = []
    for item in data['items']:
        # result_industries = result_sub_industries = result_income_streams = website = 'none'
        industries = [item_ind['name'] for item_ind in item['industries']]
        result_industries = ', '.join(industries)

        sub_industries = [item_sub_ind['name'] for item_sub_ind in item['sub_industries']]
        result_sub_industries = ', '.join(sub_industries)

        income_streams = [inc_stream['name'] for inc_stream in item['income_streams']]

        revenues = [rev['name'] for rev in item['revenues']]

        result_income_streams = ', '.join(income_streams + revenues)
        website = get_single_company(item['path'])
        to_csv.append([item['name'], result_industries, result_sub_industries, result_income_streams, website,
                       item['hq_locations'][0]['address'],
                       item['startup_ranking_rating'],
                       item['employee_6_months_growth_relative'],
                       f"{item['launch_month']}-{item['launch_year']}",
                       f"{item['latest_valuation_enhanced']['valuation_min']} - {item['latest_valuation_enhanced']['valuation_max']}"
                       ])
    with open('ireland_dealroom_co.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_csv)


#---------------------------------------------------------------------------------------
def api_request(offset):
    global proxy_data
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR5RXVHSXRVcThZYkRSUVpUVDVoOCJ9.eyJodHRwczovL2RlYWxyb29tLmNvL3VzZXJfdXVpZCI6IjI4N2ZlN2I1LTFlZTYtNGRiNC04ZDk2LWMxYzc2MzcxYzY2OSIsImh0dHBzOi8vZGVhbHJvb20uY28vcm9sZXMiOlsic3RhbmRhcmQiXSwiaHR0cHM6Ly9kZWFscm9vbS5jby9lbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaHR0cHM6Ly9kZWFscm9vbS5jby9pc19zb2NpYWwiOnRydWUsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZGVhbHJvb20uY28vIiwic3ViIjoibGlua2VkaW58cjZYTGNEdks1SiIsImF1ZCI6WyJodHRwczovL2FwaS5kZWFscm9vbS5jby9hcGkvdjIiLCJodHRwczovL2RlYWxyb29tLXByb2R1Y3Rpb24uZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcyODU4ODQ5MSwiZXhwIjoxNzI4Njc0ODkxLCJzY29wZSI6Im9wZW5pZCIsImF6cCI6IjJiUzhYT3NjQXpwbDdnSVlPRzFlNURodWZmNU84Z3QzIiwicGVybWlzc2lvbnMiOltdfQ.EsebFPdxtotrzW4eNlez3cQ7tY1DVXA8pjgaqaEMrzZ5ZSqdajJxqWKiskh56tFQ3sCR3zWrNEtZMMt3BSKfmnHi7EvA6XBjtb9rW4KvE_ZiManDDw1JAf5CgZqTyNeRocNdl8wN5aLMVwc-4up1p8MGz8Sl3Sw6f4ZVn4tzyLPyIbVFyQgaJrUauZba_QZJpc1iUGMRWUzdFSYY02tYIUputNGACyu45Ii4JtB1E6-V3fM86pD-dW609qZaAjxnQG1kb4Xx2ysIp-Ape6xWQSoG_lk_Gs6tMG1VTBYB1qD5bl4OR7Mq6uOrdc2QyonhXmsQPs-vJDtfKNxSNl2Dww',
        'content-type': 'application/json',
        'origin': 'https://ireland.dealroom.co', #differ_from
        'priority': 'u=1, i',
        'referer': 'https://ireland.dealroom.co/', #differ_from
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-dealroom-app-id': '060623092', #differ_from
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'fields': 'uuid,appstore_app_id,client_focus,company_status,corporate_industries,employees_chart,employees_latest,employees,entity_sub_types,employee_12_months_growth_percentile,employee_12_months_growth_unique,similarweb_12_months_growth_percentile,similarweb_12_months_growth_unique,similarweb_12_months_growth_delta,similarweb_12_months_growth_relative,similarweb_3_months_growth_delta,similarweb_3_months_growth_percentile,similarweb_3_months_growth_relative,similarweb_3_months_growth_unique,similarweb_6_months_growth_delta,similarweb_6_months_growth_percentile,similarweb_6_months_growth_relative,similarweb_6_months_growth_unique,facebook_url,founders,growth_stage,hq_locations,income_streams,industries,innovations_count,investments,investors,is_editorial,kpi_summary,latest_valuation_enhanced,launch_month,launch_year,linkedin_url,lists_ids,lists,name,patents_count,path,playmarket_app_id,revenues,sdgs,service_industries,similarweb_chart,sub_industries,tags,tagline,technologies,total_funding_enhanced,type,tech_stack,twitter_url,employee_12_months_growth_delta,employee_12_months_growth_relative,employee_3_months_growth_delta,employee_3_months_growth_percentile,employee_3_months_growth_relative,employee_3_months_growth_unique,employee_6_months_growth_delta,employee_6_months_growth_percentile,employee_6_months_growth_relative,employee_6_months_growth_unique,founders_score_cumulated,founders,founders_top_university,founders_top_past_companies,fundings,has_strong_founder,has_super_founder,images,innovations,innovation_corporate_rank,is_ai_data,ipo_round,latest_revenue_enhanced,matching_score,past_founders_raised_10m,past_founders,startup_ranking_rating,total_jobs_available,year_became_unicorn,year_became_future_unicorn,job_roles',
        'limit': 25,
        'offset': offset,
        'form_data': {
            'must': {
                'filters': {
                    'founding_or_hq_slug_locations': {   #differ_from
                        'values': [
                            'ireland',
                            'northern_ireland',
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
                'company_status': [
                    'closed',
                ],
            },
        },
        'multi_match': True,
        'keyword_match_type': 'fuzzy',
        'sort': '-startup_ranking_rating',
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

    data = response.json()
    return data


#---------------------------------------------------------------------------------------


with open('ireland_dealroom_co.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["name", "industries", "sub_industries", "type", "website", "location","signal","grouth","launch Date","valuation"])

data = api_request(0)

# print(data)
try:
    total_companies = data['total']
except:
    print(data)
    print("IP BANNED!!")
    sys.exit(0)



print(f'TOTAL COMPANIES {total_companies}')
items_on_page(data)

for i in range(25, total_companies, 25):
    data = api_request(0)
    items_on_page(data)
    print(f'-----------------------------DONE {i}/{total_companies}')
    time.sleep(2.5)
