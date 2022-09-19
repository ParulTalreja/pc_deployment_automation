import urllib

import requests
import json
import re
import urllib3
urllib3.disable_warnings()
from urllib.request import urlopen





def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #target_url='http://10.41.24.115:9000/scheduled_deployments/2022-08-31/630fa0b173101a6b4ea5a4da/deployments/630fa0b173101a6b4ea5a4dd/DEPLOY/630fa0b173101a6b4ea5a4dd_1.txt'

    target_url='http://10.41.24.115:9000/scheduled_deployments/2022-09-12/631ebc3482e14f8c022bf9cb/deployments/631ebc3482e14f8c022bf9cd/DEPLOY/631ebc3482e14f8c022bf9cd_1.txt'
    searchException(target_url)
    searchIPAddress(target_url)
    pe_collated_log_url='http://10.41.24.115:9000/scheduled_deployments/2022-09-12/631ebc3482e14f8c022bf9cb/deployments/631ebc3482e14f8c022bf9cd/entity_logs/retry_0/collated_logs_pe/pc_deployment_logs_from_pe_10.40.164.175.log'
    searchPEInfo(pe_collated_log_url)


def searchPEInfo(pe_collated_log_url):
    response = urllib.request.urlopen(pe_collated_log_url)
    important = []
    test = []
    startIndex=0
    endIndex=0
    keep_phrases = ["\"operation_type\"",
                    "\"weight\"",
                    ]
    for index, line in enumerate(response):
        line = line.decode(errors='ignore')
        if "\"operation_type\"" in line:
            startIndex=index
        if "\"weight\"" in line:
            endIndex=index
        if(startIndex>endIndex and startIndex!=0):
            #print("startIndex: ",startIndex)
            #print("endIndex: ",endIndex)
            important.append(line.strip())
            startIndex=startIndex+1
        if(startIndex==endIndex and startIndex!=0):
            #print("Test startIndex: ", startIndex)
            #print("Test endIndex: ", endIndex)
            #test=json.dumps(important)
            test.append(important)
            #print(test)
            important=[]
            endIndex=endIndex+1

    #print(len(test))
    print(*test, sep='\n')

    # for index, line in enumerate(response):
    #     line = line.decode(errors='ignore')
    #     for phrase in keep_phrases:
    #         if phrase in line:
    #             important.append(index)
    #             break
    #     if (index>=413 and index<=428):
    #         test += line
    # print(important)
    # print(test)



    # for line in urllib.request.urlopen(pe_collated_log_url):
    #     line = line.decode(errors='ignore')
    #
    #     if re.search(r'Ergon_', line, re.S):
    #         x = line.split("Ergon_")
    #         print(x)
    #         # print('Exception Message', line)


def searchException(target_url):
    for line in urllib.request.urlopen(target_url):
        line = line.decode('utf-8')
        word = 'Exception'
        # print('line Number:', line)
        #  word1 = ''
        if line.find(word) == 0:
            print('Exception Message', line)

def searchIPAddress(target_url):
    response=urllib.request.urlopen(target_url)
    string_found=False
    string_found_index=0;
    for index, line in enumerate(response):
        line = line.decode('utf-8')
        if re.search(r'Starting One click Deployment creation', line, re.S):
            string_found=True
            string_found_index=index
        if (string_found and index == string_found_index+2):
            #print(line)
            x = line.split(":{")
            string = '{' + x[1]
            obj = json.loads(string)
            pc_vm_list=obj['resources']['pc_vm_list']
            for item in pc_vm_list:
                print("PC IP List:", item['nic_list'][0]['ip_list'])






# Press ⌘F8 to toggle the breakpoint.
if __name__ == '__main__':
    print_hi('PyCharm')