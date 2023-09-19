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

def fetch_traceback(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR"):
    #fetches m,n lines (not just error specific lines) before and after all instaces of matching error pid
    str = ""
    with open(filename, "r", encoding="latin-1", newline="") as f:
        before = collections.deque(maxlen=linesBefore)
        
        for line in f:
            if errorPrefix in line:
                for item in before:
                    str += item
                str += line
                for item in itertools.islice(f, linesAfter):
                    str+=item
                str +="\n"
            before.append(line)
        return str

def fetch_traceback_first(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR"):
    #fetches m,n lines (not just error specific lines) before and after first instace of matching error pid
    str = ""
    with open(filename, "r", encoding="latin-1", newline="") as f:
        before = collections.deque(maxlen=linesBefore)
        
        for line in f:
            if errorPrefix in line:
                for item in before:
                    str += item
                str += line
                for item in itertools.islice(f, linesAfter):
                    str+=item
                str +="\n"
                break
            before.append(line)
        return str

def fetch_traceback_firstX(filename, linesBefore=3, linesAfter=3, X=2, errorPrefix="ERROR"):
        #fetches m,n lines (not just error specific lines) before and after first X instaces of matching error pid
    str = ""
    count=0
    with open(filename, "r", encoding="latin-1", newline="") as f:
        before = collections.deque(maxlen=linesBefore)
        
        for line in f:
            if errorPrefix in line:
                for item in before:
                    str += item
                str += line
                for item in itertools.islice(f, linesAfter):
                    str+=item
                str +="\n"
                count+=1
                if count>=X:
                    break
            before.append(line)
        return str

def fetch_traceback_last(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR"):
    str = ""
        #fetches m,n lines (not just error specific lines) before and after last instace of matching error pid
        #backward file read module was not working. We can improve the time complexity by using that later
    with open(filename, "r", encoding="latin-1", newline="") as f:
        noErrors=0
        for line in f:
            if errorPrefix in line:
                noErrors+=1
        count=0
    f.close()
    with open(filename, "r", encoding="latin-1", newline="") as f:
        before = collections.deque(maxlen=linesBefore)
        for line in f:
            if errorPrefix in line:
                count+=1
                if count > noErrors-1:
                    for item in before:
                        str += item
                    str += line
                    for item in itertools.islice(f, linesAfter):
                        str+=item
                    str +="\n"
                before.append(line)
    return str 

def fetch_traceback_lastY(filename, linesBefore=3, linesAfter=3, Y=2, errorPrefix="ERROR"):
    #fetches m,n lines (not just error specific lines) before and after all last Y instaces of matching error pid
    #backward file read module was not working. We can improve the time complexity by using that later

    str = ""

    with open(filename, "r", encoding="latin-1", newline="") as f:
        noErrors=0
        for line in f:
            if errorPrefix in line:
                noErrors+=1
        count=Y-1
    f.close()
    #counting al errors and then printing the last Y ones. We are parsing twice which is inefficient. Scope for improvement using FileReadBackwards
    with open(filename, "r", encoding="latin-1", newline="") as f:
        before = collections.deque(maxlen=linesBefore)
        for line in f:
            if errorPrefix in line:
                count+=1
                if count > noErrors-1: 
                    for item in before:
                        str += item
                    str += line
                    for item in itertools.islice(f, linesAfter):
                        str+=item
                    str +="\n"
                    
                before.append(line)
    return str 




#print (fetch_traceback_last())
#print (fetch_traceback_lastY())
#print (fetch_traceback_last(filename='/Users/abhishek.jalan/Desktop/Nutanix/pc_deployment_automation/prism_gateway.log', errorPrefix="ERROR"))
#print (fetch_traceback_last())