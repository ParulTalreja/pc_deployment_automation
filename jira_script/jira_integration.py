from jira import JIRA


jira_server= "https://jira.nutanix.com/"
jira_options={"server":jira_server}

token ="NjkwNjk0Mjk3MDc5OimnLJznESBme8NXhoVefy0ILi8S"
username = "medha.bajpai@nutanix.com"


jira = JIRA(options=jira_options, token_auth=token)

def create_jira_issue(summary, description):
  issue_dict = \
    {

      "project": {"key": "ENG"},
      "summary": summary,
      "description": description,
      "customfield_15160": {"value" : "None"}, #component
      "issuetype": {"name": "Bug"},
      "priority": {"name": "Critical - P1"},
      "versions": [{"name": "master"}],
      "customfield_13260": {"value" : "No"},  # Regression?
      "fixVersions": [{"name": "master"}],
      "customfield_10011" : [{"value" : "Usability"}], # impact
      "customfield_20084" : {"value" : "Not Applicable"} # Bug Found With?
    }
  new_issue = jira.create_issue(fields=issue_dict)
  print("new issue: {}".format(new_issue))
  return new_issue

def filter_jira_issue(summary):

  query = 'Summary ~ "' + summary + '"'
  issues = jira.search_issues(query)

  for issue in issues:
    print(issue.key)
    print("----")

  return issues


# def main():
#   pass

# if __name__ == "__main__":
#   main()