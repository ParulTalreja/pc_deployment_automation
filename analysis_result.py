class analysis_result:
  def __init__(self, message_list, jira):
    self.message_list = message_list
    self.jira = jira

class message:
  def __init__(self, text, code):
    self.text = text
    self.code = code
