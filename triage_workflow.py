import json
import re
import urllib3
urllib3.disable_warnings()
import os
from file_read_backwards import FileReadBackwards
from lib import download_util, util


def _find_error_thread_id_in_file(dir_name, file_name, searchContent):
    with open(os.path.join(dir_name, file_name), mode='r', encoding='latin-1') as fp:
        for l_no, line in enumerate(fp):
            # search string
            if searchContent in line:
                error_thread_id = re.findall(r'\b\d{5,}\b', line)
                print('line',line)
                break
        return ''.join(error_thread_id)

def _find_error_msg_in_logfile(dir_name, file_name , searchContent):
    with open(os.path.join(dir_name, file_name), mode='r', encoding='latin-1') as fp:
        previous_line = None
        for l_no, line in enumerate(fp):
            # search string
            if searchContent in line:
                return previous_line+line
            else:
                previous_line = line



def find_error_msg_in_logfile_using_threadId(dir_name, file_name, error_thread_id):
    count = 0
    errorlogs = ''
    loglevel='ERROR '
    file_url=dir_name+file_name
    with FileReadBackwards(file_url,encoding="latin-1") as frb:
        for line in frb:
            if (loglevel + error_thread_id) in line:
                return line
        print("Error message not found in %s", file_name)


def _collects_log_from_file(downloaded_log_location,logFileName, searchContent):
    if(logFileName=="prism_gateway.log"):
        error_msg=_find_error_msg_in_logfile(downloaded_log_location,logFileName,searchContent)
        print(error_msg)
    else:
        error_thread_id=_find_error_thread_id_in_file(downloaded_log_location,logFileName,searchContent)
        print("Thread Id: ",error_thread_id)
        error_msg=find_error_msg_in_logfile_using_threadId(downloaded_log_location,logFileName,error_thread_id)
    checksum_string = util.remove_uuid_digits_from_string(error_msg)
    chksm = util.get_checksum_without_caching(checksum_string)
    #print("Checksum for string: {0} is {1}".format(checksum_string, chksm))
    chksm_mapping_available= util.retrieve_value_from_json(chksm)
    if(not chksm_mapping_available):
        util.update_json_with_checksum(chksm, searchContent)
        print("No Existing Result found based on checksum")
    else:
        print(chksm_mapping_available)
        return chksm_mapping_available




def pc_deploy_debug_mapping(errorMessage,PC_LOG_URL,PE_LOG_URL):
    dir_name = "triage_rules/"
    file_name = "pc_deploy_debug_mapping.json"
    mapping_found = False
    with open(os.path.join(dir_name, file_name), "r") as f:
        pc_deployment_error_list = json.load(f)
        for i in pc_deployment_error_list['pc.deployment']:
            if(errorMessage in i['exception_summary'] or errorMessage.find(i['exception_summary'])!=-1):
                mapping_found = True
                log_signature=i['log_signature']
                use_for_checksum=i['use_for_checksum']
                # Case 1- Direct Deflect Issue
                if not use_for_checksum:
                    return i['response']
                else:
                    cluster_log = i['cluster_log'] #possible values PC/PE/PC,PE
                    if(PC_LOG_URL==""):
                        print("PC LOGS NOT FOUND")
                        exit(-1)
                    if "PC" in cluster_log:
                        #downloaded_log_location="resources/home/nutanix/data/logs/"
                        downloaded_log_location= download_util.download_pc_logs(PC_LOG_URL)
                    if(PE_LOG_URL==""):
                        print("PE LOGS NOT FOUND")
                        exit(-1)
                    if "PE" in cluster_log:
                        downloaded_log_location= download_util.zip_download_and_extract(PE_LOG_URL)

                    for logFileName in i['file_lst']:
                        _collects_log_from_file(downloaded_log_location,logFileName, i['log_signature'])
                    return None


        if(not mapping_found):
            print("Log Signature not found in pc debug mapping")



# if __name__ == "__main__":
#     errorMessage="Failed while enabling CMSP: Encountered error in cmsp sub task 'IAMv2 Migration & Bootstrap':"
#     PC_LOG_URL='http://10.41.24.125:9000/scheduled_deployments/2023-08-29/64edf55f82e14f4f40d436b2/deployments/64edf55f82e14f4f40d436b4/entity_logs/retry_0/10.37.110.97/logbay_PC-10.37.110.97_1693329010/'
#     PE_LOG_URL='http://10.41.24.125:9000/scheduled_deployments/2023-08-29/64edf55f82e14f4f40d436b2/deployments/64edf55f82e14f4f40d436b4/entity_logs/retry_0/auto_cluster_prod_f348cf370366/logbay_auto_cluster_prod_f348cf370366_1693328666/'
#     print(pc_deploy_debug_mapping(errorMessage,PC_LOG_URL,PE_LOG_URL))