import json
import csv
from curl_cffi import requests
import time


class DealRoomJsonHandler:

    def __init__(self,csv_path):
        self.csv_path = csv_path

    def start_from_file(self, file_name):
        with open(f'berlin_files/{file_name}.json', 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)

    def saveJson(self):
        with open(f'berlin_files/1.json', 'w', encoding='utf-8') as file:
            json.dump(self.json_data, file, ensure_ascii=True, indent=4)

    def nodev(self):
        return ' -skip- '

    def write_first_row(self, data_row):
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(data_row)

    # column functions =============================================================================

    def colMarket(self, client_focus, industries, sub_industries):
        raw_market = [item['name'].replace('business', 'B2B').replace('consumer', 'B2C') for item in client_focus]
        focus = raw_market

        raw_industries = [item['name'] for item in industries]
        raw_sub_industries = [item['name'] for item in sub_industries]

        return ' ,'.join(focus + raw_industries + raw_sub_industries)

    def colType(self, tehnologies, income_streams, revenues):
        raw_tehnologies = [item['name'] for item in tehnologies]
        raw_streams = [item['name'] for item in income_streams]
        raw_revenues = [item['name'] for item in revenues]

        return ' ,'.join(raw_tehnologies + raw_streams + raw_revenues)

    def colLaunch(self, launch_month, launch_year):
        months = ["x", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        if None != launch_month:
            # return int(launch_month)
            return f'{months[int(launch_month)]} {launch_year}'
        return launch_year

    def colValuation(self, latest_valuation_enhanced):
        if None == latest_valuation_enhanced:
            return "no val"
        return latest_valuation_enhanced['valuation_currency'] + " " + str(latest_valuation_enhanced['valuation'])

    def colFunding(self, total_funding_enhanced):
        return total_funding_enhanced['currency'] + " " + str(total_funding_enhanced['amount'])

    def colLocation(self, hq_locations):
        city = ''
        country = ''
        if None == hq_locations:
            return 'hhh'
        raw_location = hq_locations[0]
        city = raw_location.get("city", "{}")
        # print(city)
        if None != city:
            city = city.get("name", "")
        else:
            city = ''
        country = raw_location.get("country", "{}").get("name", "")
        return (city + ' ' + country).strip()

    def lastRound(self, fundings):

        if len(fundings) < 1:
            return "no data"
        max_year = 0
        co = 0
        co_max_year = 0
        for fun in fundings:

            if fun['year'] >= max_year:
                max_year = fun['year']
                co_max_year = co
            co += 1

        return f"{fundings[co_max_year]['round']}, {fundings[co_max_year]['currency']} {fundings[co_max_year]['amount']}"

    def colJobopenings(self, job_roles):
        return ' ,'.join(job_roles[0:2])

    def colSharePrice(self, kpi_sumary):
        if len(kpi_sumary['share_price_chart']) > 0:
            # sh_price = kpi_sumary['share_price_chart']
            return f'{kpi_sumary['share_price_currency']} {kpi_sumary['share_price_chart'][-1]['value']}'
        else:
            return '-'

    def colEquityValue(self, kpi_sumary):
        if len(kpi_sumary['valuations']) > 0:
            equi = kpi_sumary['valuations'][-1]
            return f' {equi['valuation_currency']} {equi['market_cap']}'
        else:
            return '-'

    def colEnterpriseValue(self, latest_valuation_enhanced):
        if None == latest_valuation_enhanced:
            return "no data"
        valuation = latest_valuation_enhanced.get("valuation", 'non')
        if 'non' != valuation:
            return f"{latest_valuation_enhanced['valuation_currency']} {valuation}"
        else:
            return "no data"

    def colEvRevenue2020(self, kpi_summary):
        values = kpi_summary.get("values", "[]")
        if len(values) < 1:
            return "-"
        for v in values:
            if v['year'] == 2020:
                if v['ev_revenue'] is not None:
                    return f"{v['ev_revenue']}"
        return '-'

    def colEvRevenue2021(self, kpi_summary):
        values = kpi_summary.get("values", "[]")
        if len(values) < 1:
            return "-"
        for v in values:
            if v['year'] == 2021:
                if v['ev_revenue'] is not None:
                    return f"{v['ev_revenue']}"
        return '-'

    def colEvRevenue2022(self, kpi_summary):
        values = kpi_summary.get("values", "[]")
        if len(values) < 1:
            return "-"
        for v in values:
            if v['year'] == 2022:
                if v['ev_revenue'] is not None:
                    return f"{v['ev_revenue']}"
        return '-'

    def colEvEbitda2020(self, kpi_summary):
        values = kpi_summary.get("values", "[]")
        if len(values) < 1:
            return "-"
        for v in values:
            if v['year'] == 2020:
                if v['ev_ebitda'] is not None:
                    return f"{v['ev_ebitda']}"
        return '-'

    def colEvEbitda2021(self, kpi_summary):
        values = kpi_summary.get("values", "[]")
        if len(values) < 1:
            return "-"
        for v in values:
            if v['year'] == 2021:
                if v['ev_ebitda'] is not None:
                    return f"{v['ev_ebitda']}"
        return '-'

    def colEvEbitda2022(self, kpi_summary):
        values = kpi_summary.get("values", "[]")
        if len(values) < 1:
            return "-"
        for v in values:
            if v['year'] == 2022:
                if v['ev_ebitda'] is not None:
                    return f"{v['ev_ebitda']}"
        return '-'

    def colIpoDate(self, ipo_round):
        if ipo_round is None:
            return "-"
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ipo_year = ipo_round.get("year", "0")
        ipo_month_raw = ipo_round.get("month", "0")

        if int(ipo_month_raw) > 0:
            ipo_month = months[int(ipo_month_raw)]
        else:
            ipo_month = ''
        return f'{ipo_month} {ipo_year}'.strip()

    # column functions END =========================================================================


    def startup_website(self, company_id):
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

        # proxies = {
        #     'http': proxy_data,
        #     'https': proxy_data
        # }

        response = requests.get(
            f'https://api.dealroom.co/api/v2/entities/{company_id}?fields=about,about_ai_generated,affiliated_funds,appstore_app_id,can_edit,career_page_url,client_focus,closing_month,closing_year,company_status,corporate_industries,country_experience,current_and_prev_year_fundings_num,delivery_method,employees_chart,employees_latest,employee_12_months_growth_percentile,employee_12_months_growth_unique,similarweb_12_months_growth_percentile,similarweb_12_months_growth_unique,employees,entity_sub_types,exits_higher_800m,facebook_url,fundings_investor,growth_stage,hq_locations,uuid,images(100x100),income_streams,industries,industry_experience,innovations_count,investments_higher_800m,investments_num,investments,investor_exits_funding_enhanced,investor_exits_num,investor_total_rank,investor_total,investors,is_ai_data,is_editorial,is_government,is_non_profit,is_from_traderegister,job_offers_total,kpi_summary,landscapes,latest_valuation_enhanced,launch_month,launch_year,legal_entities,linkedin_url,lists_ids,lists,lp_investments,lp_investors,name,ownerships,patents_count,path,playmarket_app_id,revenues,rounds_experience,sdgs,service_industries,share_ticker_symbol,similarweb_chart,similarweb_hidden,sub_industries,tagline,tags,team_total,tech_stack,technologies,total_funding_enhanced,traffic(top_countries,visitors,sources),twitter_url,instagram_handle,type,website_url&limit=25&offset=0',
            headers=headers,
            # proxies=proxies,
            impersonate="chrome101",
        )
        single_data = response.json()

        print(f'requesting {company_id}')
        time.sleep(0.5)  #Use pauses to avoid being banned
        return single_data['website_url']


    # startup_website END =========================================================================

    def main_function(self, json_data, first_loop=False):
        to_csv = []
        for item in json_data['items']:
            company_data = {
                "Name": item['name'],
                "Dealroom signal": item['startup_ranking_rating'],
                "Market": self.colMarket(item['client_focus'], item['industries'], item['sub_industries']),
                "Type": self.colType(item['technologies'], item['income_streams'], item['revenues']),
                "Growth 12 months growth": self.nodev(),  # -------------------------------------------------------skip
                "Launch date": self.colLaunch(item['launch_month'], item['launch_year']),
                "Valuation": self.colValuation(item['latest_valuation_enhanced']),
                "Funding": self.colFunding(item['total_funding_enhanced']),
                "Location": self.colLocation(item['hq_locations']),
                "Last Round": self.lastRound(item['fundings']['items']),
                "No. of job openings": item['total_jobs_available'],
                "Job openings": self.colJobopenings(item.get("job_roles", "{}")),
                "Revenue": "skip",  # -------------------------------------------------------------------------skip
                "Status": item['company_status'],
                "Growth Stage": item['growth_stage'],
                "Monthly web visits": 'skip',  # -------------------------------------------------------------------skip
                "Alumni who became founders that raised more than €10m": item['past_founders_raised_10m'],
                "Web visits change in rank": item['similarweb_12_months_growth_delta'],
                "Employees change in rank": item['employee_12_months_growth_delta'],
                "Corporate Innovation Ranking": item['innovation_corporate_rank'],
                "Share Price": self.colSharePrice(item['kpi_summary']),
                "Equity value": self.colEquityValue(item['kpi_summary']),
                "Enterprise Value": self.colEnterpriseValue(item.get("latest_valuation_enhanced", "{}")),
                "EV/Revenue (2020)": self.colEvRevenue2020(item['kpi_summary']),
                "EV/Revenue (2021)": self.colEvRevenue2021(item['kpi_summary']),
                "EV/Revenue (2022)": self.colEvRevenue2022(item['kpi_summary']),
                "EV/EBITDA (2020)": self.colEvEbitda2020(item['kpi_summary']),
                "EV/EBITDA (2021)": self.colEvEbitda2021(item['kpi_summary']),
                "EV/EBITDA (2022)": self.colEvEbitda2022(item['kpi_summary']),
                "IPO DATE": self.colIpoDate(item.get("ipo_round", "{}")),
                "Logo Image": item['images']['74x74'],
                "tagline": item['tagline'],
                # "website": self.startup_website(item['path'])
            }
            if first_loop:
                self.write_first_row(list(company_data.keys()))

            to_print = list(company_data.values())
            print([to_print[0]] + to_print[26:])
            to_csv.append(to_print)

        with open(self.csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(to_csv)


