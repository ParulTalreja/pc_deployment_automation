from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from start_autotriage_deployment_bot import start_bot_analysis
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = App(token="xoxb-2172428722-5834253288615-dWUKruIiNCeXJOGElVUBlAcV")

# @app.event({
#      "type": "message",
#      # "subtype": "message_changed"
#  })
# def pc_deployment_reply(event, say):
#      # if "@something" in event["text"].lower():
#      print(event["text"])
#      say(text="Able to get messages", channel = "C05QMNCHTLN")

@app.event("app_mention")
def pc_mention_reply(event, say):
    msg = event["text"][event["text"].find("> ")+3:-1]
    print(msg)
    result_analysis = start_bot_analysis(msg)
    print(result_analysis)
    say(text = result_analysis, channel = "C05QMNCHTLN")

if __name__ == "__main__":
    SocketModeHandler(app, "xapp-1-A05QUUW297F-5847906674434-c5b52f13b5d321e91b17e4f7a66b97d12c066998c91a5509d8343f4dd6b13883").start()

