import urllib
import json
import re
import urllib3
import ast
import hashlib
urllib3.disable_warnings()
from urllib.request import urlopen


def searchException(target_url):
    try:
        response = urllib.request.urlopen(target_url)
        for index, line in enumerate(response):
            line = line.decode('utf-8')
            word = 'Exception'
            if line.find(word) == 0:
                x = line.split("Exception:")
                x[1] = ast.literal_eval(x[1])
                message = extractErrorMessageFromString(x[1])
                return message
            else:
                word = 'NuTestInterfaceError:'
                if line.find(word) == 0 :
                    x = line.split(word)
                    return x[1].strip()
    except Exception as e:
        error = "Encountered Exception in checking deployment logs: %s" % str(e)
        print(error)




def extractErrorMessageFromString(exceptionMessage):
    def none_to_empty_str(items):
        return {k: v if v is not None else '' for k, v in items}

    json_str = json.dumps(exceptionMessage)
    exceptionJson = json.loads(json_str, object_pairs_hook=none_to_empty_str)
    message = exceptionJson['failure_analysis']['message']
    sub_error_msg="Error message:"
    if sub_error_msg in message:
        x = message.split("Error message:")
        return x[1].strip()
    return message



def searchIPAddress(target_url):
    response = urllib.request.urlopen(target_url)
    string_found = False
    string_found_index = 0;
    pc_ip_list = []
    for index, line in enumerate(response):
        line = line.decode('utf-8')
        if re.search(r'Starting One click Deployment creation', line, re.S):
            string_found = True
            string_found_index = index
        if (string_found and index == string_found_index + 2):
            # print(line)
            x = line.split(":{")
            string = '{' + x[1]
            # print(string)
            obj = json.loads(string)
            pc_vm_list = obj['resources']['pc_vm_list']
            for item in pc_vm_list:
                pc_ip_list.append(item['nic_list'][0]['ip_list'])
    return pc_ip_list


def remove_uuid_digits_from_string(msg):
  """
    It will Remove Numbers ,special and UUID from String
  Args:
    msg(string): string on which want to remove
  Returns:
    strings:
  """
  #print(msg)

  # Remove test name if exists
  if 'Timeout executing method - test_' in msg:
    temp = msg.split('test_')[1].split(' ')[0]
    msg = msg.replace(temp, '')

  cluster_pat_lst = [
    "[u']*auto_cluster_prod[\w]*", "auto_pc_[\w]*", "auto_cluster_[\w]*",
    "cluster:auto_cluster_[\w]*", 'name="auto_cluster_[\w]*',
    'cluster-name="[\w]*"']

  exp_pat_lst = [
    "0x[\w]*>:", "\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", "[^A-Za-z]+",
    'cloud-type="[\w-]*"', 'name="nutest_cred[\w-]*"',
    "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}, \[[\w\-\'\]\)]*"]

  entity_pat_lst = [
    "[A-Za-z0-9_-]*nu_vm_[A-Za-z0-9_-]*", "[N|n]utest_[\w]*",
    "nutest_vm[\w]*", "nu_vm_[\w]*", "Brownfield_UVM_[\w]*", "Windows_[\w]*",
    "VM : [\w|,| |:|-]*", 'name="nutest[\w_]*"', 'name="ncc[\w_]*"',
    'nutest_metro[\w"]*', 'nutest_rp_[\w]*', '[w|W]indows[\w]*']

  extras_pat_lst = [
    "\['aut[\w\-\'\]\)]*", "\['aut[\w\-\'\, \'\]\)]*",
    "uhura_Restore_[\w]*", "ReplTest_vaai_[\w]*",
    "nutest_protect_cloned[\w]*", "FailHostRestorePdTest[\w]*",
    "{'ctr_name': u'nutest[\w|_|'|,| |:|}|)]*",
    "client.egg-tmp/stats[\w|/]*", "client.egg-tmp/zeus[\w|/]*",
    "test_cloud_[\w]*", "vlan[\w]*", "Recovery Plan[:| |\w]*"]

  for pat in cluster_pat_lst + exp_pat_lst + entity_pat_lst + extras_pat_lst:
    regex = re.compile(pat)
    msg = re.sub(regex, '', msg)

  return msg


def get_checksum_without_caching(msg):
  """
    Gets the message and returns the checksum
  Args:
    msg(string): msg to be used for calculating the checksum
  Returns:
    (string) checksum of the msg
  """
  hasher = hashlib.md5()
  hasher.update(msg.encode('utf-8'))
  return hasher.hexdigest()


def update_json_with_checksum(key,value):
    # Load the existing JSON data
    with open("triage_rules/result.json", "r") as json_file:
        existing_data = json.load(json_file)
    # Add a new key-value pair
    existing_data[key] = value
    # Write the updated data back to the JSON file
    with open("triage_rules/result.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)  # Optional: indent for pretty formatting


def retrieve_value_from_json(key_to_retrieve):
    # Read the data from the JSON file
    with open("triage_rules/result.json", "r") as json_file:
        loaded_data = json.load(json_file)

    # Retrieve content based on key
    if key_to_retrieve in loaded_data:
        value = loaded_data[key_to_retrieve]
        print(f"{key_to_retrieve}: {value}")
        return value
    else:
        print(f"Key '{key_to_retrieve}' not found in the JSON data.")
        return False

# if __name__ == "__main__":
#     target_url= 'http://10.41.24.115:9000/scheduled_deployments/2023-08-29/64edbfc982e14f1dd16678be/deployments/64edbfc982e14f1dd16678bf/DEPLOY/64edbfc982e14f1dd16678bf_1.txt'
#     searchException(target_url)