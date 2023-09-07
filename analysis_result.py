class analysis_result:
  def __init__(self, message_list, ask_jira=False):
    self.message_list = message_list
    self.ask_jira = ask_jira


class message:
  def __init__(self, text, code):
    self.text = text
    self.code = code
