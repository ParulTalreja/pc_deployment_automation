import urllib

import requests
import json
import re
import urllib3
urllib3.disable_warnings()
from urllib.request import urlopen
import os
from file_read_backwards import FileReadBackwards
import hashlib

#This File will have triaging workflow
# Search for error in file..process the string based on Thread Id and calculate hash based on checksum( SHA-256)



#This method will find the error stacktrace with its threadID
def _find_error_thread_id_in_file(dir_name, file_name, searchContent):
    with open(os.path.join(dir_name, file_name), mode='r', encoding='latin-1') as fp:
        for l_no, line in enumerate(fp):
            # search string
            if searchContent in line:
                error_thread_id = re.findall(r'\b\d{5,}\b', line)
                print('line',line)
                break
        return ''.join(error_thread_id)


def get_checksum_of_string(errorlogs):
    hashed_string = hashlib.sha256(errorlogs.encode('utf-8')).hexdigest()
    print(hashed_string)


def _find_checksum_based_on_thread_id(dir_name, file_name, error_thread_id):
    count = 0
    errorlogs = ''
    with FileReadBackwards("/Users/parultalrejaaggarwal/PycharmProjects/pythonProject/genesis.out",
                           encoding="latin-1") as frb:
        for line in frb:
            if error_thread_id in line:
                count += 1
                errorlogs += line
                if (count >= 15):
                    break;
        return get_checksum_of_string(errorlogs)


def _find_exception_in_logFile(logFileName, searchContent):
    dir_name="/Users/parultalrejaaggarwal/PycharmProjects/pythonProject/"
    #TO-DO: This is an array.can have multiple files in file name
    file_name=logFileName
    error_thread_id=_find_error_thread_id_in_file(dir_name,file_name,searchContent)
    print(error_thread_id)
    _find_checksum_based_on_thread_id(dir_name,file_name,error_thread_id)







def pc_deploy_debug_mapping():
    ergon_error_message="deploy msp:failed to deploy the ntnx dvp: Operation timed out"
    dir_name = "/Users/parultalrejaaggarwal/PycharmProjects/pythonProject/triage_rules/failed_rules/"
    file_name = "pc_deploy_debug_mapping.json"
    with open(os.path.join(dir_name, file_name), "r") as f:
        pc_deployment_error_list = json.load(f)
        #print("dep stages : {}".format(pc_deployment_error_list))
        for i in pc_deployment_error_list['pc.deployment']:
            if(ergon_error_message in i['exception_summary']):
                cluster_log = i['cluster_log']
                #cluster_log=pe/pc TODO-Add logic for using pc/pe log location
                for logFileName in i['file_lst']:
                    #print(logFileName)
                    _find_exception_in_logFile(logFileName,i['exception_summary'])


pc_deploy_debug_mapping()
