import json
import re
import collections
import itertools
import sys
import urllib
import json
import re
import ast
import hashlib
from datetime import datetime
from analysis_result import response, message

def get_last_stage_passed(analysis_result,clusterFile, genesisFile, ispc):
    timestamp=None
    stageLine=None
    stage=None
    with open("stages.json", "r") as j:
        stage_list= json.load(j)
        i=0
        logMessage=stage_list["stages"][i]['logMessage']
        #print(logMessage)
        if clusterFile is not None:
            if ispc:
                analysis_result.message_list.append(message("Checking PC Cluster File.", None))
            else:
                analysis_result.message_list.append(message("Checking PE Cluster File.", None))
            with open(clusterFile, "r", encoding='latin-1') as f:
                for line in f:
                    if(line.find(logMessage)!=-1):
                        timestamp=line[0:24]
                        stageLine=line
                        stage=stage_list["stages"][i]
                        i=i+1
                        logMessage=stage_list["stages"][i]['logMessage']
                    if(i==2):
                        break
                f.close()
        else:
            analysis_result.message_list.append(message("Cluster File does not exist", None))
        if i==2:
            if genesisFile is not None:
                if ispc:
                    analysis_result.message_list.append(message("PC Cluster Stages Passed. Checking PC Genesis File.", None))
                else:
                    analysis_result.message_list.append(message("PE Cluster Stages Passed. Checking PE Genesis File.", None))
                with open(genesisFile,"r", encoding="latin-1") as f:
                    for line in f:
                        if(line.find(logMessage)!=-1):
                            timestamp=line[0:24]
                            stageLine=line
                            stage=stage_list["stages"][i]
                            i=i+1
                            logMessage=stage_list["stages"][i]['logMessage']
                    f.close()

    return timestamp, stageLine, stage

# timestamp, stageLine, stage=get_last_stage_passed("cluster_config.out.20230905-193554Z","genesis.out.20230905-192856Z")
# print(timestamp)
# print(stageLine)
# print(stage)

def get_trace_after_last_stage(analysis_result,peclusterFile, pegenesisFile,pcclusterFile, pcgenesisFile):
    timestamp, stageLine, stage=get_last_stage_passed(analysis_result,peclusterFile,pegenesisFile,0)
    analysis_result.message_list.append(message(stage["name"] + " PASSED.", None))
    if(stage['stageNo.']>'2' and pegenesisFile is not None):
        analysis_result.message_list.append(message("TRACEBACK OF PE GENESIS FILE", None))
        #genesisFile
        str = ""
        with open(pegenesisFile, "r", encoding="latin-1", newline="") as f:
            before = collections.deque(maxlen=15)

            for line in f:
                if stageLine in line:
                    break
            
            for line in f:
                if "Traceback" in line:
                    for item in before:
                        str += item
                    str += line
                    for item in itertools.islice(f, 15):
                        str+=item
                    str +="\n"
                    break
                before.append(line)
            
            analysis_result.message_list.append(message(None, str))
            
    elif(peclusterFile is not None):
        analysis_result.message_list.append(message("TRACEBACK OF PE CLUSTER FILE", None))
        #clusterFile
        str = ""

        with open(peclusterFile, "r", encoding="latin-1", newline="") as f:
            before = collections.deque(maxlen=15)

            for line in f:
                if stageLine in line:
                    break
            
            for line in f:
                if "Traceback" in line:
                    for item in before:
                        str += item
                    str += line
                    for item in itertools.islice(f, 15):
                        str+=item
                    str +="\n"
                    break
                before.append(line)
            
            analysis_result.message_list.append(message(None, str))
    return analysis_result, "Failed after "+stage["name"], str
    #if stage["pc_check"]:



#get_trace_after_last_stage("cluster_config.out.20230905-193554Z","genesis.out.20230905-192856Z","","")