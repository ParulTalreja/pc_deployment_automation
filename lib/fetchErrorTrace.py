# "Should be able to download X lines before and Y lines after the matched line as well. 
#Also have ability to find matched 1st instance, last instaces, all instances, first X matched instances and last Y matched instances.
# fetch_traceback(filename, [linesBefore], [linesAfter], [numberOfMatches]) "
import collections
import itertools
import sys
import urllib
import json
import re
import ast
import hashlib

#filename="/Users/abhishek.jalan/Desktop/Nutanix/pc_deployment_automation/aplos.out"
#errorPrefix="ERROR 92378960"
#errorMessage="ERROR 92378960 genesis_utils.py:3035 Unable to fetch cluster_functions from cached config_proto"

#filename="/Users/abhishek.jalan/Desktop/Nutanix/pc_deployment_automation/prism_gateway.log"

def fetch_error_lines(filename, errorPrefix):
#fetch all lines  from the log file with a specific error pid
    str = ""
    with open(filename, "r", encoding="latin-1", newline="") as f:  
        str=[]
        for line in f:
            if errorPrefix in line:
                str.append(line)
    return str

def fetch_error_traceback(filename, linesBefore=3, linesAfter=3, errorPrefix="", errorMessage=""):
#fetch all m,n lines of specific error pid before and after all instaces of matching error message 
    f= fetch_error_lines(filename, errorPrefix)
    str = ""
    for line in f:
            if errorMessage in line:
                i=f.index(line)
                istart=max(0,i-linesBefore)
                iend=min(len(f),i+linesAfter+1)
                for j in range(istart,iend):
                    str+=f[j]
                str +="\n"
    if(len(str)==0): return "No Match found"

    return str

def fetch_error_traceback_firstX(filename, linesBefore=3, linesAfter=3, errorPrefix="", errorMessage="", X=2):
#fetch all m,n lines of specific error pid before and after first X instaces of matching error message 
    f= fetch_error_lines(filename, errorPrefix)
    str = ""
    count=0
    for line in f:
            if errorMessage in line:
                if(count>=2): break
                i=f.index(line)
                istart=max(0,i-linesBefore)
                iend=min(len(f),i+linesAfter+1)
                for j in range(istart,iend):
                    str+=f[j]
                str +="\n"
                count+=1
    if(len(str)==0): return "No Match found"
         
    return str

# def fetch_error_traceback_lastY(filename='/Users/abhishek.jalan/Desktop/Nutanix/pc_deployment_automation/genesis.out.20230831-171521Z', linesBefore=3, linesAfter=3, errorPrefix="ERROR 92378960", errorMessage="ERROR 92378960 genesis_utils.py:3035 Unable to fetch cluster_functions from cached config_proto", Y=2):
# #fetch all m,n lines of specific error pid before and after last Y instaces of matching error message 
#     f= fetch_error_lines(filename, errorPrefix)
#     str = ""
#     count=0
#     numErrors=0
#     for line in f:
#         if errorMessage in line:
#              numErrors+=1

#     for line in f:
#             if errorMessage in line:
#                 count+=1
#                 if count<numErrors-Y+1: continue
#                 i=f.index(line)
#                 istart=max(0,i-linesBefore)
#                 iend=min(len(f),i+linesAfter+1)
#                 for j in range(istart,iend):
#                     str+=f[j]
#                 str +="\n"
#                 count+=1
      
#     return str

def fetch_error_traceback_lastY(filename, linesBefore=3, linesAfter=3, errorPrefix="",errorMessage="", X=2):
#fetch all m,n lines of specific error pid before and after last Y instaces of matching error message 
    f= fetch_error_lines(filename, errorPrefix)
    str = ""
    count=0
    for line in reversed(f):
            if errorMessage in line:
                if(count>=2): break
                i=f.index(line)
                istart=max(0,i-linesBefore)
                iend=min(len(f),i+linesAfter+1)
                for j in range(istart,iend):
                    str+=f[j]
                str +="\n"
                count+=1
    if(len(str)==0): return "No Match found"
                
    return str



#print(fetch_error_lines())
#print(fetch_error_traceback(filename="/Users/abhishek.jalan/Desktop/Nutanix/pc_deployment_automation/aplos.out", errorPrefix="ERROR", errorMessage=""))
print(fetch_error_traceback_firstX(filename="/Users/abhishek.jalan/Desktop/Nutanix/pc_deployment_automation/prism_gateway.log", errorPrefix="ERROR"))
#print(fetch_error_traceback_firstX())
#print(fetch_error_traceback_lastY())