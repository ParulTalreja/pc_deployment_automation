import urllib

import requests
import json
import re
import urllib3
urllib3.disable_warnings()
from urllib.request import urlopen



#This File reads the deployment logs and Collated PE logs. Parse the logs and fetch the necessary information like Exception Message, PC IP address and Task information

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #target_url='http://10.41.24.115:9000/scheduled_deployments/2022-08-31/630fa0b173101a6b4ea5a4da/deployments/630fa0b173101a6b4ea5a4dd/DEPLOY/630fa0b173101a6b4ea5a4dd_1.txt'

    target_url='http://10.41.24.115:9000/scheduled_deployments/2022-09-22/632c57b957f2f36ab3aaba57/deployments/632c57b957f2f36ab3aaba59/DEPLOY/632c57b957f2f36ab3aaba59_1.txt'
    #searchException(target_url)
    searchIPAddress(target_url)
    pe_collated_log_url='http://10.41.24.115:9000/scheduled_deployments/2022-09-22/632c57b957f2f36ab3aaba57/deployments/632c57b957f2f36ab3aaba59/entity_logs/retry_0/collated_logs_pe/pc_deployment_logs_from_pe_10.22.184.14.log'
    searchPEInfo(pe_collated_log_url)


def searchPEInfo(pe_collated_log_url):
    response = urllib.request.urlopen(pe_collated_log_url)
    test = []
    startIndex=0
    endIndex=0
    output = "{"

    keep_phrases = ["\"message\"",
                    "\"weight\"",
                    ]
    for index, line in enumerate(response):
        line = line.decode(errors='ignore')
        if "\"message\"" in line:
            startIndex=index
        if "\"weight\"" in line:
            endIndex=index
        if(startIndex>endIndex and startIndex!=0):
            line=line.strip()
            output=output+line
            startIndex=startIndex+1
        if(startIndex==endIndex and startIndex!=0):
            output = output + line.strip() + "}"
            test.append(output)
            output="{"
            endIndex=endIndex+1

    print(*test, sep='\n')
    for i in test:
        obj = json.loads(i)
        operation_type = obj['operation_type']
        status= obj['status']
        # if(status=="kFailed"):
        #     print('Operation Type:',operation_type,'Task UUID:',obj['uuid'],'Subtask_UUID:',obj['subtask_uuid_list'])


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
            #print(string)
            obj = json.loads(string)
            pc_vm_list=obj['resources']['pc_vm_list']
            for item in pc_vm_list:
                print("PC IP List:", item['nic_list'][0]['ip_list'])






# Press ⌘F8 to toggle the breakpoint.
if __name__ == '__main__':
    print_hi('PyCharm')