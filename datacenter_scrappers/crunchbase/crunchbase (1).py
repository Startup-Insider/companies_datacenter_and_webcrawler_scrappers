import subprocess
import requests
import json
import threading
import time
import sys
import os
import base64
import csv
import websocket  #  pip install websocket-client

# ----------------------------- variables that must be changed

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
url = 'https://www.crunchbase.com/discover/saved/companies-europe-since-2013-for-scraper/d0e6679a-15e5-4fd9-ab56-90c6c3774afb'

csv_path = 'crunchbase.csv'
delay_time = 5

# ----------------------------- variables that must be changed END


work_path = '/'.join(csv_path.split('/')[:-1])
if len(work_path) > 0:
    work_path = work_path + '/'
unique_startup = set()
browser_socket_address, tab_socket_address = None, None
ws_tab = None
stop_scraper = False


# --------------------------------------------------function start -----------------------------------------------------
def check_browser():
    global browser_socket_address
    try:
        response = requests.get('http://localhost:9222/json/version', timeout=(1, 1))
        response.raise_for_status()
        data = response.json()
    except:
        return False
    browser_socket_address = data['webSocketDebuggerUrl']
    return True


# --------------------------------------------------function END -------------------------------------------------------
def run_browser():
    flags = [
        "--remote-debugging-port=9222",
        "--remote-allow-origins=http://localhost:9222",
    ]
    command = [chrome_path] + flags
    subprocess.Popen(command)


# --------------------------------------------------function END -------------------------------------------------------
def get_ws_tab():
    global tab_socket_address
    try:
        response = requests.get('http://localhost:9222/json', timeout=1)
        tab_data = response.json()
        response.raise_for_status()
    except:
        print("[error] CAN`T GET JSON ROUTE CHROME")
        return False
    for td in tab_data:
        if 'page' == td['type']:
            tab_socket_address = td['webSocketDebuggerUrl']
            break
    return True


# --------------------------------------------------function END -------------------------------------------------------

def on_message(ws, message):
    message_json = json.loads(message)
    if 'id' in message_json:
        drive_id_requests(message_json)

    if 'method' in message_json:
        if 'Fetch.requestPaused' == message_json['method']:
            drive_fetch_request(message_json)


def on_error(ws, error):
    print(f"[function_on_error]: {error}")
    print(f"Error type: {type(error)}")
    print(f"Error details: {error}")
    print(f"Error details: {repr(error)}")


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


def on_open(ws):
    print("Connected to Browser")


def run_socket():
    global ws_tab
    ws_tab = websocket.WebSocketApp(
        tab_socket_address,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws_tab.run_forever()


# --------------------------------------------------function END -------------------------------------------------------

def drive_fetch_request(msg):
    global ws_tab

    if 'organization.companies' in msg['params']['request']['url']:
        ws_tab.send(json.dumps({
            "id": 222,
            "method": "Fetch.getResponseBody",
            "params": {
                "requestId": msg['params']['requestId']
            }
        }))

    ws_tab.send(json.dumps({
        "id": 333,
        "method": "Fetch.continueRequest",
        "params": {
            "requestId": msg['params']['requestId']
        }
    }))


# --------------------------------------------------function END -------------------------------------------------------
def click_next():
    global ws_tab
    js_code = """ 
(function() { const element = document.querySelector('a[aria-label=\"Next\"]');
if(!element){
return {href:false,isDisabled:true};
}
     const href = element.getAttribute('href'); 
     const isDisabled = element.hasAttribute('disabled'); 
    if(isDisabled !== true){
     element.click();} return { href, isDisabled }; })()
    """
    ws_tab.send(json.dumps({
        "id": 444,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_code,
            "returnByValue": True
        }
    }))


# --------------------------------------------------function END -------------------------------------------------------
def json_to_csv(startup_data):
    global csv_path,delay_time
    to_return = []
    for sd in startup_data['entities']:
        st_name = sd['properties']['identifier']['value']

        if st_name in unique_startup:
            print(f"skiping {st_name} [already in csv]")
            continue
        unique_startup.add(st_name)

        try:
            st_website = sd['properties']['website']['value']
        except:
            print("no website for " ,st_name)
            st_website = "none"
        try:
            st_category_groups = ",".join([cg["value"] for cg in sd['properties']['category_groups']])
        except:
            st_category_groups = "none"
        try:
            st_categories = ",".join([ct["value"] for ct in sd['properties']['categories']])
        except:
            st_categories = "none"

        st_shot_desc = sd['properties']['short_description']

        try:
            st_num_investors = sd['properties']['num_investors']
        except:
            st_num_investors = 'none'

        st_founded_on = sd['properties']['founded_on']['value']
        to_return.append([st_name, st_website, st_category_groups, st_categories, st_num_investors,
                          st_founded_on, st_shot_desc])
        print(st_name, ": ", st_website)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(to_return)
    time.sleep(delay_time)
    click_next()


# --------------------------------------------------function END -------------------------------------------------------
def array_to_str(var_array):
    to_return = ", ".join([va for va in var_array])


# --------------------------------------------------function END -------------------------------------------------------
def drive_id_requests(message_json):
    global stop_scraper
    if 222 == message_json['id']:
        temp_data_startup = base64.b64decode(message_json['result']['body'])
        startup_data = json.loads(temp_data_startup.decode('utf-8'))
        json_to_csv(startup_data)
        # with open('crunchbase.json','w') as file:
        #     file.write(json.dumps(startup_data))
    if 444 == message_json['id']:
        # print(message_json['result']['result']['value']['href'])
        # print(message_json['result']['result']['value']['isDisabled'])
        if message_json['result']['result']['value']['isDisabled']:
            print("----  The last page has been reached.")
            stop_scraper = True
        if message_json['result']['result']['value']['href']:
            manage_url_write(f"https://www.crunchbase.com{message_json['result']['result']['value']['href']}")


# --------------------------------------------------function END -------------------------------------------------------
def manage_url_read():
    global url, work_path
    try:
        with open(f'{work_path}crunchbase_page.txt', 'r') as file:
            url = file.read()
    except:
        print(f'file {work_path}crunchbase_page.txt NOT FOUND go to default url')


# --------------------------------------------------function END -------------------------------------------------------
def manage_url_write(new_url):
    global work_path
    with open(f'{work_path}crunchbase_page.txt', 'w') as file:
        file.write(str(new_url))


# --------------------------------------------------function END -------------------------------------------------------
def verify_url_not_stoped():
    global work_path
    try:
        with open(f'{work_path}crunchbase_page.txt', 'r') as file:
            return file.read()
    except:
        return "zero"


# --------------------------------------------------function END -------------------------------------------------------
def create_new_csv():
    global csv_path
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'name', 'website', 'category_groups', 'categories', 'num_investors',
            'founded_on', 'shot_desc'
        ])


# --------------------------------------------------function END -------------------------------------------------------


manage_url_read() # to start from memorised url
error_text = """\nERROR CONNECT TO BROWSER, PLEASE CLOSE ALL CHROME WINDOWS AND TRY AGAIN
[ when the scraper starting, no Chrome windows should be open ]."""

if not check_browser():
    run_browser()

if not check_browser():
    print(error_text)
    sys.exit(0)

if not get_ws_tab():
    sys.exit(0)

if os.path.exists(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        saved_startups = csv.reader(csvfile)
        try:
            next(saved_startups)
        except:
            create_new_csv()
        for row in saved_startups:
            unique_startup.add(row[0])
else:
    print('creating new csv')
    create_new_csv()


thread = threading.Thread(target=run_socket)
thread.start()

time.sleep(0.6)

# url = input("Enter the start url: ")

ws_tab.send(json.dumps({"id": 1, "method": "Fetch.enable", "params": {"patterns": [{"requestStage": "Response"}]}}))
ws_tab.send(json.dumps({
    "id": 2,
    "method": "Page.navigate",
    "params": {"url": url}
}))

time.sleep(10)

js_code_login = """ 
(function() { 
const emailInput = document.querySelector('input[name="email"]');

if(emailInput){
emailInput.value = 'jan.thomas@startup-insider.com';
emailInput.dispatchEvent(new Event('input'));

const passwordInput = document.querySelector('input[name="password"]');
passwordInput.value = 'm&Cg5GTSeC2Kq!u';
passwordInput.dispatchEvent(new Event('input'));

setTimeout(() => {
    const loginButton = document.querySelector("button.login");
    loginButton.click();
}, 1000); 
}}
)()
"""
ws_tab.send(json.dumps({
        "id": 445,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_code_login,
            "returnByValue": True
        }
 }))



floating_url = None
count_while = 0
try:
    while True:
        if stop_scraper:
            break
        count_while += 1
        time.sleep(1)
        verify_period = verify_url_not_stoped()
        if (count_while % 15) == 0:
            count_while = 0
            if floating_url == verify_period:
                click_next()
            else:
                floating_url = verify_period
except KeyboardInterrupt:
    pass
    # print("Exiting...")
finally:
    if ws_tab:
        # print("close WebSocket...")
        ws_tab.close()
    thread.join()
    print("scrapper stopped.")
