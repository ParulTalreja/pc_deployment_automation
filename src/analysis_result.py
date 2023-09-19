class response:
  def __init__(self, message_list, ask_jira=False,jira_summary="",jira_description = ""):
    self.message_list = message_list
    self.ask_jira = ask_jira
    self.jira_summary=jira_summary
    self.jira_description = jira_description


  def __str__(self):
    messages_str = "\n".join(str(message) for message in self.message_list)
    return f"\n{messages_str}, \nJira: {self.ask_jira}"


class message:
  def __init__(self, text=None, code=None):
    self.text = text
    self.code = code

  def __str__(self):
    return f" {self.text} {self.code}"



