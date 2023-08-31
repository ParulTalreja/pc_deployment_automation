import requests
import json
import re
import urllib3
import triage_workflow
urllib3.disable_warnings()
from lib import util
import sys
import time

def start_autotriage_deployment_bot():
    """
    execute python start_autotriage_deployment_bot.py <RDM Link> <PC LogURL> <PE LogURL>
    :return:
    """
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python start_autotriage_deployment_bot.py RDMLink PCLogURL PELogURL")
        return

    rdm_link= sys.argv[1]
    pc_log_url = sys.argv[2]
    pe_log_url = sys.argv[3]
    print("RDM link:", rdm_link)
    print("PC Log URL:", pc_log_url)
    print("PE Log URL:", pe_log_url)
    pc_deployment = PCAutoDeployment(rdm_link,pc_log_url,pe_log_url)
    bot_start_time = time.time()
    pcdeploymentlogLocation = pc_deployment._get_failed_deployment_logurl(rdm_link)
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
    def __init__(self, RDM_URL,PC_LOG_URL,PE_LOG_URL):
        self.RDM_URL = RDM_URL


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
        failedDeploymentLogUrl= log_link + "deployments/" + failed_deployment_id + "/DEPLOY/"+deploymentFileName
        #print(failedDeploymentLogUrl)
        return failedDeploymentLogUrl

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

