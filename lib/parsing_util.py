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


def fetch_line_regex_from_file(fileName, query):
    """
    Parsing logs for a specific regex
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        query: example: Timestamp 2023-08-25 21:55:34,651, string match
    Returns: All matched lines
    """
    str=""
    with open(fileName, "r", encoding="latin-1", newline="") as f:
        target_string = f.readline()
        for target_string in f:
            result = re.search(query, target_string)
            if not result is None:
                str+=target_string
    return str


def read_between_timestamps_python(log_file,start_timestamp,end_timestamp):
    logs = []
    within_time_range = False
    start_timestamp = datetime.strptime(start_timestamp,"%Y-%m-%d %H:%M:%S")
    end_timestamp = datetime.strptime(end_timestamp,"%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file,'r') as file:
            for line in file:
                parts = line.strip().split(' ',2)
                if(len(parts)>=2):
                    timestamp_str = parts[0]+' '+parts[1]
                    try:
                        timestamp = datetime.strptime(timestamp_str,"%Y-%m-%d %H:%M:%S,%fZ")
                    except ValueError:
                        if within_time_range:
                            logs.append(line)
                            continue
                    try:
                        if start_timestamp<=timestamp<=end_timestamp:
                            logs.append(line)
                            within_time_range = True
                        elif within_time_range:
                            break
                    except UnboundLocalError:
                        continue
                elif within_time_range:
                    logs.append(line)
    except FileNotFoundError:
        print("File not Found")
    if len(logs)==0:
        print("No logs found")
    return logs



def read_between_timestamps_java(log_file,start_timestamp,end_timestamp):
    logs = []
    within_time_range = False
    start_timestamp = datetime.strptime(start_timestamp,"%Y-%m-%d %H:%M:%S")
    end_timestamp = datetime.strptime(end_timestamp,"%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file,'r') as file:
            for line in file:
                parts = line.split()
                if(len(parts)>=3):
                    timestamp_str = parts[1]+' '+parts[2]
                    try:
                        timestamp = datetime.strptime(timestamp_str,"%Y-%m-%d %H:%M:%S,%fZ")
                    except ValueError:
                        if within_time_range:
                            logs.append(line)
                            continue
                    try:
                        if start_timestamp<=timestamp<=end_timestamp:
                            logs.append(line)
                            within_time_range = True
                        elif within_time_range:
                            break
                    except UnboundLocalError:
                        continue
                elif within_time_range:
                    logs.append(line)
    except FileNotFoundError:
        print("File not Found")

    if len(logs)==0:
        print("No logs found")
    return logs

#variations of parsing utils for fetching some M & N lines before and after errror prefixes

def fetch_error_lines(filename, errorPrefix):
#fetch all lines  from the log file with a specific error pid
    str = ""
    with open(filename, "r", encoding="latin-1", newline="") as f:  
        str=[]
        for line in f:
            if errorPrefix in line:
                str.append(line)
    return str

def fetch_error_traceback(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR", errorMessage=""):
    """
    Fetch all m,n lines of specific error pid before and after all instances of matching error message
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367"
        errorMessage: any error string (RDM exception summary string)

    Returns: return matched lines

    Example: if the errorPrefix="ERROR 897367" and the logs have lines in this order:
    ..
    L1  INFO.....
    L2  WARNING.....
    L3  ERROR 897367 <some error messsage>      Here is this error message is matched, and the error prefix is "ERROR 897367"
    L4  INFO......                              Suppose we need 2 lines before and after matched msg with the prefix. Here, there are mo
    L5  ERROR 897365                            matching lines before L3 and only one (L5) after L3. So only L3 and L5 are returned.       
    L6  INFO.....

    """


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

def fetch_error_traceback_firstX(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR", errorMessage="", X=2):
    """
    Returns m,n lines of specific error which is First X matches of instances
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367"
        errorMessage: any error string (RDM exception summary string)

    Returns: return matched lines

    """

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

def fetch_error_traceback_lastY(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR",errorMessage="", X=2):
#fetch all m,n lines of specific error pid before and after last Y instaces of matching error message 
    """
    Returns m,n lines of specific error which are the Last Y matches of instances
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367"
        errorMessage: any error string (RDM exception summary string)

    Returns: return matched lines which contain the error message and the X, Y lines conatining the error prefix
    """
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

# FOLLOWING ARE GENERIC IMPLEMENTAIONS WHICH RETURN TRACEBACK CONTAINING ALL MESSAGES
# AND NOT JUST ERROR MESSAGES FOR THE MATCHING ERROR PREFIX

def fetch_traceback(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR"):
    """
    Fetches X lines before all instances of the matched string and Y lines after matched string stored in errrorPrefix but these X and Y lines returned respectively are not
    checked for the error prefix.
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367". A specific error message can also be used here (RDM exception summary string)
    Returns: returns the matched lines and X and Y no of lines before and after the matched lines

    Example: if the errorPrefix="ERROR 897367" and the logs have lines in this order:
    ..
    L1  INFO.....
    L2  WARNING.....
    L3  ERROR 897367    ( Here, this is a first matched instance and we need 2 lines before and after matched prefix 
    L4  INFO......         "ERROR 897367; Lines L1 to L5 will be returned. Here L1, L2, L4 donot contain the same error prefix
    L5  ERROR 897365        After this, Line L5 is also matched, so Lines L3 to L7 will also be returned & son on)
    L6  INFO.....
    """
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

def fetch_traceback_first_matched_instance(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR"):
    #fetches m,n lines (not just error specific lines) before and after first instace of matching error pid
    """
    Fetches X lines before matched string and Y lines after the first instance of the matched string stored in errrorPrefix but these X and Y lines returned respectively are not
    checked for the error prefix.
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367". A specific error message can also be used here (RDM exception summary string)
    Returns: returns the first matched line with error message and X and Y no of lines before and after the matched lines

    """
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

def fetch_traceback_firstM(filename, linesBefore=3, linesAfter=3, X=2, errorPrefix="ERROR"):
        #fetches m,n lines (not just error specific lines) before and after first X instaces of matching error pid
    """
    Fetches X lines before matched string and Y lines after matched string for first M instances of the matched string stored in errrorPrefix but these X and Y lines returned respectively are not
    checked for the error prefix.
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367". A specific error message can also be used here (RDM exception summary string)
    Returns: returns the first M instances of the matched lines and X and Y number of lines before and after the matched lines in order

    """
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

def fetch_traceback_last_matched_instance(filename, linesBefore=3, linesAfter=3, errorPrefix="ERROR"):
    str = ""
    """
    Fetches X lines before and Y lines after the last instance of the matched string stored in errrorPrefix but these X and Y lines returned respectively are not
    checked for the error prefix.
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367". A specific error message can also be used here (RDM exception summary string)
    Returns: returns the last instance of the matched line and X and Y no of lines before and after the matched line

    """
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

def fetch_traceback_lastM(filename, linesBefore=3, linesAfter=3, Y=2, errorPrefix="ERROR"):
    """
    Fetches X lines before matched string and Y lines after matched string for last M instances of the matched string stored in errrorPrefix but these X and Y lines returned respectively are not
    checked for the error prefix.
    Args:
        fileName: complete path of file example: resources/nutest_2023-08-25_22_31_54-2023-08-25-81114631834-10.37.109.88-CW/cvm_logs/aplos.FATAL
        linesBefore: X Line Before the errorMessage starting with errorPrefix
        linesAfter: Y Line after the errorMessage starting with errorPrefix
        errorPrefix: Example "ERROR 897367". A specific error message can also be used here (RDM exception summary string)
    Returns: returns the last M instances of the matched lines and X and Y number of lines before and after the matched lines in order

    """

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