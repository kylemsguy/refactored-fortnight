import os
import time
from slackclient import SlackClient
from db import Session as session
from models.people import User

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

def handle_command(command, channel):
	"""
		gets commands directed at bot, determines if valid.
		if so then acts on commands
		if not returns whats needed for clarification
	"""
	response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
		"* command with numbers, delimited by spaces."
	if command.startswith(EXAMPLE_COMMAND):
		response = "Sure ... write some more code and I can do that!"
	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
	"""
		The Slack Real Time Messaging API is an events firehose.
		this parsing function returns None unless a message is
		directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				## return text after the @ mention, w/o whitespace
				return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
	return None, None

def send_message(channel_id, message):
	# channel_id can also be the form @username (all lowercase)
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=message,
		username='hackthewest',
		# icon_emoji=':lenny:' # optional
	)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 #1 sec delay b/w reading from firehose
    if slack_client.rtm_connect():
            print("StarterBot connected and running!")
            while True:
                    command, channel = parse_slack_output(slack_client.rtm_read())
                    if command and channel:
                            handle_command(command, channel)
                    time.sleep(READ_WEBSOCKET_DELAY)
    else:
            print("Connection failed. Invalid Slack token or bot ID?")
