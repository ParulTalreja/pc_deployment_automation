import json
import re
import urllib3

from start_autotriage_deployment_bot import analysis_result

urllib3.disable_warnings()
import os
from file_read_backwards import FileReadBackwards
from lib import download_util, util
import stage_extraction
from analysis_result import response, message



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


def _collects_log_from_file(downloaded_log_location,logFileName, searchContent , rdm_error_checksm):
    if(logFileName=="prism_gateway.log"):
        error_msg=_find_error_msg_in_logfile(downloaded_log_location,logFileName,searchContent)
        analysis_result.message_list.append(
            message("Found below error in log", error_msg))
        #print(error_msg)
    else:
        error_thread_id=_find_error_thread_id_in_file(downloaded_log_location,logFileName,searchContent)
        print("Thread Id: ",error_thread_id)
        error_msg=find_error_msg_in_logfile_using_threadId(downloaded_log_location,logFileName,error_thread_id)
    file_msg_chcksum = util.get_checksum_of_errorstring(error_msg)
    #Get combined checksum of RDM error message and logfile message
    chksm = util.get_checksum_without_caching(rdm_error_checksm+file_msg_chcksum)

    #print("Checksum for string: {0} is {1}".format(checksum_string, chksm))
    chksm_mapping_available= util.retrieve_value_from_json(chksm)
    if(not chksm_mapping_available):
        util.update_json_with_checksum(chksm, searchContent)
        return "No Existing Result found based on checksum"
    else:
        #print(chksm_mapping_available)
        analysis_result.message_list.append(
            message("Below is the error root cause", chksm_mapping_available))

        return analysis_result

def get_log_files_for_staging(parent_path):
    files = os.listdir(parent_path)
    sorted_files = sorted(files)
    last_genesis_out = None
    last_cluster_config_out = None
    for file_name in sorted_files:
        if(file_name == "genesis.out"):
            last_genesis_out =  file_name
            break
        if(file_name.find('genesis.out') != -1):
            last_genesis_out = file_name
    for file_name in sorted_files:
        if(file_name == "cluster_config.out"):
            last_cluster_config_out =  file_name
            break

        if(file_name.find('cluster_config.out') != -1):
            last_cluster_config_out = file_name

    return parent_path+"/"+last_cluster_config_out, parent_path+"/"+last_genesis_out


def pc_deploy_debug_mapping(errorMessage,PC_LOG_URL,PE_LOG_URL,deployment_id):
    dir_name = "triage_rules/"
    file_name = "pc_deploy_debug_mapping.json"
    mapping_found = False
    rdm_error_checksm=util.get_checksum_of_errorstring(errorMessage)
    pc_log_location = ""
    pe_log_location = ""
    with open(os.path.join(dir_name, file_name), "r") as f:
        pc_deployment_error_list = json.load(f)
        for i in pc_deployment_error_list['pc.deployment']:
            if(errorMessage in i['exception_summary'] or errorMessage.find(i['exception_summary'])!=-1):
                mapping_found = True
                log_signature=i['log_signature']
                use_for_checksum=i['use_for_checksum']
                # Case 1- Direct Deflect Issue
                if not use_for_checksum:
                    analysis_result.message_list.append(
                        message("This is known issue. Please Follow below suggestions", i['response']))
                    return analysis_result
                else:
                    cluster_log = i['cluster_log'] #possible values PC/PE/PC,PE
                    if "PC" in cluster_log:
                        if (PC_LOG_URL == ""):
                            return "PC LOGS NOT FOUND"
                        #downloaded_log_location="resources/home/nutanix/data/logs/"
                        downloaded_log_location= download_util.download_pc_logs(PC_LOG_URL,deployment_id)
                        analysis_result.message_list.append(
                            message("Mapping is found. Downloading PC logs",))
                        #downloaded_log_location= (download_util_multithreaded.download_pc_logs(PC_LOG_URL))[0]
                    if "PE" in cluster_log:
                        if (PE_LOG_URL == ""):
                            return "PE LOGS NOT FOUND"
                        analysis_result.message_list.append(
                            message("Mapping is found. Downloading PE logs", ))
                        downloaded_log_location= download_util.zip_download_and_extract(PE_LOG_URL,deployment_id)
                        #downloaded_log_location= (download_util_multithreaded.download_multithreaded(PE_LOG_URL))[0]

                    for logFileName in i['file_lst']:
                        analysis_result.message_list.append(
                            message("Looking into logfile"+logFileName))
                        return _collects_log_from_file(downloaded_log_location,logFileName, i['log_signature'],rdm_error_checksm)



        if(not mapping_found):
            pc_cluster_config_log_location = ""
            pc_genesis_log_location = ""
            pe_cluster_config_log_location = ""
            pe_genesis_log_location = ""
            if PC_LOG_URL!="":
                pc_log_location = download_util.download_pc_logs(PC_LOG_URL,deployment_id)
                pc_cluster_config_log_location, pc_genesis_log_location = get_log_files_for_staging(pc_log_location)
            if PE_LOG_URL!="":
                pe_log_location = download_util.download_pc_logs(PE_LOG_URL,deployment_id)
                pe_cluster_config_log_location, pe_genesis_log_location = get_log_files_for_staging(pe_log_location)

            analysis_result.message_list.append(
                message("Log Signature not found in pc debug mapping", ))
            #Add here stage which was successfull+ file name for analysis

            traceback=stage_extraction.get_trace_after_last_stage(pe_cluster_config_log_location,pe_genesis_log_location,pc_cluster_config_log_location,pc_genesis_log_location)
            analysis_result.message_list.append(message("file name", traceback))
            return analysis_result




# if __name__ == "__main__":
#     errorMessage="Failed while enabling CMSP: Encountered error in cmsp sub task 'IAMv2 Migration & Bootstrap':"
#     PC_LOG_URL='http://10.41.24.125:9000/scheduled_deployments/2023-08-29/64edf55f82e14f4f40d436b2/deployments/64edf55f82e14f4f40d436b4/entity_logs/retry_0/10.37.110.97/logbay_PC-10.37.110.97_1693329010/'
#     PE_LOG_URL='http://10.41.24.125:9000/scheduled_deployments/2023-08-29/64edf55f82e14f4f40d436b2/deployments/64edf55f82e14f4f40d436b4/entity_logs/retry_0/auto_cluster_prod_f348cf370366/logbay_auto_cluster_prod_f348cf370366_1693328666/'
#     download_util.zip_download_and_extract(PE_LOG_URL)