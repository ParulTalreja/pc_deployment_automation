# PC Deployment automated triage

## Installing Modules Commands
sudo pip3 install requirements.txt

## Usage
please upgrade to python  3.10 or higher version to use this.

upgrade using homebrew (if on older versions): 

brew install python3
brew update && brew upgrade python
alias python=/usr/local/bin/python3

python3 start_autotriage_deployment_bot.py

Execute via below command

python start_autotriage_deployment_bot.py --rdmurl = <RDM_URL>


Example:
 python3 start_autotriage_deployment_bot.py https://rdm.eng.nutanix.com/scheduled_deployments/64ec433457f2f3ac02694a18 http://10.41.24.125:9000/scheduled_deployments/2023-08-28/64ec433457f2f3ac02694a18/deployments/64ec433457f2f3ac02694a1b/entity_logs/retry_0/10.37.108.166/logbay_PC-10.37.108.166_1693218428/ http://10.41.24.125:9000/scheduled_deployments/2023-08-28/64ec433457f2f3ac02694a18/deployments/64ec433457f2f3ac02694a1b/entity_logs/retry_0/auto_cluster_prod_f38509b5355a/logbay_auto_cluster_prod_f38509b5355a_1693217740/



 Cronfile for periodic cleaning
 1. Execute the following command in virtual machine: crontab -e

 2. Edit using vim
 
 3. add the following line to the crontab file
      0 0 * * * find /home/nutanix/.venvs/bin/bin/pc_deployment_automation/resources/* -type f -mtime +7 -exec rm -r {} \; -o -type d -mtime +7 -exec /bin/rm -rf {} \;

 4. 0 0 * * * daily
    0 * * * * hourly
    * * * * * every minute
    
 5. change -mtime to desired value (no of days old)