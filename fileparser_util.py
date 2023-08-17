import urllib
import json
import re
import urllib3
import ast

urllib3.disable_warnings()
from urllib.request import urlopen


# url='http://10.41.24.115:9000/scheduled_deployments/2022-09-29/6335855857f2f3fa52949d9f/deployments/6335855857f2f3fa52949da1/DEPLOY/6335855857f2f3fa52949da1_1.txt'

def searchException(target_url):
    response = urllib.request.urlopen(target_url)
    for index, line in enumerate(response):
        line = line.decode('utf-8')
        word = 'Exception'
        if line.find(word) == 0:
            x = line.split("Exception:")
            x[1] = ast.literal_eval(x[1])
            message = extractErrorMessageFromString(x[1])
            return message


def extractErrorMessageFromString(exceptionMessage):
    def none_to_empty_str(items):
        return {k: v if v is not None else '' for k, v in items}

    json_str = json.dumps(exceptionMessage)
    exceptionJson = json.loads(json_str, object_pairs_hook=none_to_empty_str)
    message = exceptionJson['failure_analysis']['message']
    x = message.split("Error message:")
    return x[1].strip()


def searchIPAddress(target_url):
    response = urllib.request.urlopen(target_url)
    string_found = False
    string_found_index = 0;
    pc_ip_list = []
    for index, line in enumerate(response):
        line = line.decode('utf-8')
        if re.search(r'Starting One click Deployment creation', line, re.S):
            string_found = True
            string_found_index = index
        if (string_found and index == string_found_index + 2):
            # print(line)
            x = line.split(":{")
            string = '{' + x[1]
            # print(string)
            obj = json.loads(string)
            pc_vm_list = obj['resources']['pc_vm_list']
            for item in pc_vm_list:
                pc_ip_list.append(item['nic_list'][0]['ip_list'])
    return pc_ip_list
