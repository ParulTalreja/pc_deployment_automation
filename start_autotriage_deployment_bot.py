import requests
import json
import re
import urllib3
import triage_workflow
urllib3.disable_warnings()
from lib import util
import sys
import time
from bs4 import BeautifulSoup
import argparse

def list_of_strings(arg):
    return arg
def get_rdm():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rdmurl', type=list_of_strings)
    args=parser.parse_args()
    rdmlink="https://rdm.eng.nutanix.com/scheduled_deployments/"
    if(rdmlink==args.rdmurl[0:len(rdmlink)]):
        return args.rdmurl
    else:
        print("Invalid RDM link.")
        return None

def start_autotriage_deployment_bot():
    """
    execute python start_autotriage_deployment_bot.py <RDM Link> <PC LogURL> <PE LogURL>
    :return:
    """

    rdm_link= get_rdm()
    if rdm_link is None:
        return
    
    pc_deployment = PCAutoDeployment(rdm_link)
    bot_start_time = time.time()
    pcdeploymentlogLocation,pc_log_url, pe_log_url = pc_deployment._get_failed_deployment_logurl(rdm_link)
    print("RDM Link: ",rdm_link)

    if pc_log_url=="":
        print("PC LOGS NOT FOUND")
        exit(-1)
    else:
        print("PC Log URL:",pc_log_url)
        
    if pe_log_url=="":
        print("PE LOGS NOT FOUND")
        exit(-1) 
    else:
        print("PE Log URL:", pe_log_url)
    
    
    if pc_deployment.is_log_available(pcdeploymentlogLocation):
        errorMessage = util.searchException(pcdeploymentlogLocation)
        print(errorMessage)
        response = triage_workflow.pc_deploy_debug_mapping(errorMessage,pc_log_url,pe_log_url)
        analysis_competion_time= time.time()-bot_start_time
        print("Bot Analysis Completed in %s sec" % analysis_competion_time)
        print(response)
    else:
        print("Logs are not available")

class PCAutoDeployment:
    def __init__(self, RDM_URL):
        self.RDM_URL = RDM_URL

    def find_pc_link(self,URL):
        pc_log_link =  ""
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a',href = True)

        #Identifying the PC IP Address
        for link in links:
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/',link['href']):
                URL = URL + link['href']
                # print(URL)
                
        

        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a',href = True)

        for link in links:
            if re.match(r'logbay_PC.*?/',link['href']):
                pc_log_link = URL + link['href']
                # print(URL)

        return pc_log_link
    
    def find_pe_link(self,URL):
        pe_log_link =  ""
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a',href = True)

        for link in links:
            if re.match(r'auto_cluster_prod.*?/',link['href']):
                URL = URL + link['href']
                # print(URL)

        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a',href = True)

        for link in links:
            if re.match(r'logbay_auto_cluster_prod.*?/',link['href']):
                pe_log_link = URL + link['href']
                # print(URL)
        
        return pe_log_link

    def _get_failed_deployment_logurl(self, RDM_URL):
        """
        Get Failed Deployment LogUrl from RDM link.
        Args:
          RDM Link: RDM link of deployment. Example: https://rdm.eng.nutanix.com/scheduled_deployments/64dc959b57f2f3ddb46d3b4d
        Returns:
          Deploy log File url.
          Example:http://10.41.24.115:9000/scheduled_deployments/2023-08-16/64dc959b57f2f3ddb46d3b4d/deployments/64dc959b57f2f3ddb46d3b51/DEPLOY/64dc959b57f2f3ddb46d3b51_1.txt
        """
        scheduled_deployment_id = self.filter_deploymentId(RDM_URL)
        url = "https://rdm.eng.nutanix.com/api/v1/scheduled_deployments/{0}".format(scheduled_deployment_id)
        response = requests.get(url, verify=False)
        data = response.text
        actual_data = json.loads(data)
        log_link = actual_data['data']['log_link']
        deployments_id = actual_data['data']['deployments']
        failed_deployment_id=self._get_failed_deployment_id(deployments_id)
        deploymentFileName=failed_deployment_id+"_1.txt"
        baseLogPath = log_link + "deployments/" + failed_deployment_id + "/"
        failedDeploymentLogUrl= log_link + "deployments/" + failed_deployment_id + "/DEPLOY/"+deploymentFileName
        
        URL = baseLogPath+"entity_logs/"

        response = requests.get(URL)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <a> tags with an href attribute
            links = soup.find_all('a', href=True)

            for link in links:
                match = re.match(r'retry_\d+/',link['href'])
                if match:
                    URL = URL + link['href']
                    break


        PC_log_link = self.find_pc_link(URL)
        PE_log_link = self.find_pe_link(URL)
        #print(failedDeploymentLogUrl)
        return failedDeploymentLogUrl, PC_log_link, PE_log_link

    def is_log_available(self,log_url):
        r = requests.head(log_url)
        return r.status_code == 200


    def filter_deploymentId(self, RDM_URL):
        dep_id = re.search('http[s]?://.*?scheduled_deployments/([0-9a-fA-F]+)[/]?', RDM_URL)
        dep_id = dep_id.group(1)
        return dep_id

    def _get_failed_deployment_id(self,deployment_urls):
        for item in deployment_urls:
            url = "https://rdm.eng.nutanix.com/api/v1/deployments/" + item['$oid']
            response = requests.get(url, verify=False)
            actual_data = json.loads(response.text)
            status = actual_data['data']['status']
            if status == 'FAILED':
                return item['$oid']


if __name__ == "__main__":
    start_autotriage_deployment_bot()

