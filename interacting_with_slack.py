from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from start_autotriage_deployment_bot import start_bot_analysis
import ssl
import os

from time import sleep

ssl._create_default_https_context = ssl._create_unverified_context

app = App(token=os.environ["BUG_TRIAGE_BOT_BOT_TOKEN"])

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
    thread_ts = event["ts"]
    client.chat_postEphemeral(text = "_Processing your query_", channel = "C05QMNCHTLN", thread_ts = thread_ts, user=event["user"])
    print("Thread", thread_ts)
    msg = event["text"][event["text"].find("> ")+3:-1]
    print(msg)
    result_analysis = start_bot_analysis(msg)
    message_object_list = result_analysis.message_list
    ask_jira = result_analysis.ask_jira
    print("ask_jira", ask_jira)
    for message_object in message_object_list:
        if message_object.text is not None:
            client.chat_postMessage(text=message_object.text, channel="C05QMNCHTLN", thread_ts=thread_ts)
        if message_object.code is not None:
            client.chat_postMessage(text=f"```{message_object.code}```", channel="C05QMNCHTLN", thread_ts=thread_ts)
    if ask_jira:
        jira_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Create JIRA ticket?"
                }
            },
            {
                "type": "actions",
                "block_id": "jira_block",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":ticket: Create ticket"
                        },
                        "value": "create",
                        "action_id": "create_jira"
                    }
                ]
            }
        ]
        client.chat_postEphemeral(channel="C05QMNCHTLN", thread_ts=thread_ts, user=event["user"], blocks=jira_blocks)
    # print("message_list",result_analysis.message_list[0].text)
    # print(result_analysis)
    
    client.chat_postMessage(text = result_analysis, channel = "C05QMNCHTLN", thread_ts = thread_ts)
    
    sleep(2)
    
    # Ask for feedback

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hey there <@{event['user']}>! How was your experience with the me?"
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


@app.action("jira_block")
def review_bad(ack, body, client):
    ack()
    thread_ts = body["container"]["thread_ts"]
    client.chat_postEphemeral(channel="C05QMNCHTLN", thread_ts=thread_ts, user=body["user"]["id"],
                              text="Jira Ticket Raised")
    
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["BUG_TRIAGE_BOT_APP_TOKEN"]).start()
