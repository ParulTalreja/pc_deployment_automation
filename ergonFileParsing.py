import json
list1=list()
#This file parse the ergon_tasks file and build the hierarchy based on task_uuid and subtask_uuid in json format to identify the failed task.

def make_ergon_task_file_json_compatible(file_path):
    ergon_task_file = open(file_path, 'r')
    ergon_task_file_content = ergon_task_file.read()
    return json.loads(
        "[" + ergon_task_file_content.replace("}\n{", "},\n{") + "]")


def get_deployment_root_task(ergon_task_list):
    deployment_root_task_list = []
    for ergon_task in ergon_task_list:
        if (ergon_task["operation_type"] == "kPrismCentralDeploymentRequest"):
            deployment_root_task_list.append(ergon_task)
    return deployment_root_task_list


class ErgonTask:

    def __init__(self, task_dict):
        self.task_uuid = task_dict["uuid"]
        self.message = task_dict.get("message", None)
        self.response = task_dict.get("response", None)
        self.subtask_set = set()
        self.task_details = task_dict

    def add_subtask(self, subtask):
        self.subtask_set.add(subtask)


def create_ergon_task_dict(ergon_task_list):
    ergon_dict = {}
    for ergon_task in ergon_task_list:
        ergon_task_obj = ErgonTask(ergon_task)
        ergon_dict[ergon_task["uuid"]] = ergon_task_obj
    return ergon_dict



def add_subtasks_for_tasks(ergon_dict):
        for value in ergon_dict.values():
            if value.task_details.get("parent_task_uuid", None) is not None:
                ergon_dict[value.task_details["parent_task_uuid"]] \
                    .add_subtask(value)



def print_all_required_details(deployment_root_task, ergon_dict):
    root_uuid = deployment_root_task["uuid"]
    current_task = ergon_dict[root_uuid]
    return helper_function(current_task)

def helper_function(current_task):
    res_dict = {}
    res_dict["task_uuid"] = current_task.task_uuid
    res_dict["op_type"] = current_task.task_details["operation_type"]
    res_dict["message"] = current_task.message
    res_dict["response"] = current_task.response
    res_dict["status"] = current_task.task_details["status"]
    res_dict["subtask"] = list()
    for subtask in current_task.subtask_set:
        res_dict["subtask"].append(helper_function(subtask))
    return res_dict



#file_path = "/Users/vipul.gupta/Documents/nutanix/deployment_logs/nutest_2022-09-22_14_14_39-2022-09-22-51280209859-10.22.184.14-CW/cvm_logs/ergon_tasks"
file_path ="/Users/ambika/Documents/PC_Automation/pc_deployment_automation/ergon_tasks"
ergon_json_data = make_ergon_task_file_json_compatible(file_path)
deployment_task_list = get_deployment_root_task(ergon_json_data)
ergon_dict = create_ergon_task_dict(ergon_json_data)
add_subtasks_for_tasks(ergon_dict)
print(json.dumps(print_all_required_details(deployment_task_list[0], ergon_dict)))