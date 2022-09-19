# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#Identify the deployment log location

import requests
import json
import urllib3
urllib3.disable_warnings()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    response_API = requests.get('https://rdm.eng.nutanix.com/api/v1/scheduled_deployments/62fa826982e14f6b559cd768',verify=False)
    # print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    log_link = parse_json['data']['log_link']
    print("log link:\n", log_link)
    deployment_URL=parse_json['data']['deployments']
    logurl_list = []
    for item in deployment_URL:
        logurl_list.append(log_link + "deployments/"+item['$oid'] +"/DEPLOY/")

    print("Deployment URL:\n", logurl_list)






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
