from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from start_autotriage_deployment_bot import start_bot_analysis
import ssl

from time import sleep

ssl._create_default_https_context = ssl._create_unverified_context

app = App(token="xoxb-2172428722-5834253288615-yLtHilm9NQjody0UczowP8C1")

# @app.event({
#      "type": "message",
#      # "subtype": "message_changed"
#  })
# def pc_deployment_reply(event, say):
#      # if "@something" in event["text"].lower():
#      print(event["text"])
#      say(text="Able to get messages", channel = "C05QMNCHTLN")

@app.event("app_mention")
def pc_mention_reply(event, say, client):
    print("check-this")
    thread_ts = event["ts"]
    print("Thread", thread_ts)
    msg = event["text"][event["text"].find("> ")+3:-1]
    print(msg)
    result_analysis = start_bot_analysis(msg)
    print(result_analysis)
    
    client.chat_postMessage(text = result_analysis, channel = "C05QMNCHTLN", thread_ts = thread_ts)
    
    sleep(2)
    
    # Ask for feedback

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hey there <@{event['user']}>! How was your experience with RDM?"
            },
        },
        {
            "type": "actions",
            "block_id": "feedback_block",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":thumbsup: Great"
                    },
                    "style": "primary",
                    "value": "great",
                    "action_id": "review_great"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":thumbsdown: Bad"
                    },
                    "style": "danger",
                    "value": "bad",
                    "action_id": "review_bad"
                }
            ]
        }
    ]

    client.chat_postEphemeral(channel="C05QMNCHTLN", thread_ts=thread_ts, user=event["user"], blocks=blocks)


@app.action("review_great")
def review_great(ack, body, client):
    ack()
    user = body["user"]["username"]
    channel = body["channel"]["id"]
    thread_ts = body["container"]["thread_ts"]
    client.chat_postEphemeral(channel="C05QMNCHTLN", thread_ts=thread_ts, user=body["user"]["id"], text="Thank you for your feedback!")


@app.action("review_bad")
def review_bad(ack, body, client):
    ack()
    user = body["user"]["username"]
    channel = body["channel"]["id"]
    thread_ts = body["container"]["thread_ts"]
    client.chat_postEphemeral(channel="C05QMNCHTLN", thread_ts=thread_ts, user=body["user"]["id"], text="Thank you for your feedback!")
    
if __name__ == "__main__":
    SocketModeHandler(app, "xapp-1-A05QUUW297F-5851356677237-a3cf8634e69fa5ae6dde66172eab28c85a6071c37f5e43c1cf0447cd308c7c38").start()
