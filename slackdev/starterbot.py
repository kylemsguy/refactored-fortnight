import os
import time
from slackclient import SlackClient
from db import Session as session
from models.people import User

# starterbot's ID as an environment variable
BOT_ID = "U2PU5P3L4"

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

def getOrInitializeUser(userid):
	user = session.query(User).filter(User.slack_id == userid).one_or_none()
	if user is None:
		profile_info = slack_client.api_call("users.info", user=userid)
		if profile_info['ok']:
			user = User(name=profile_info['user']['profile']['first_name'], skill="nope")
		else:
			user = User(name="unknown", skill="nope")
		session.add(user)
		session.commit()
	return user


def handle_command(command, channel, message):
	"""
		gets commands directed at bot, determines if valid.
		if so then acts on commands
		if not returns whats needed for clarification
	"""
	user = getOrInitializeUser(message['user'])

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
			if output and 'text' in output:
				print(output)
			if output and 'text' in output and AT_BOT in output['text']:
				## return text after the @ mention, w/o whitespace
				return output['text'].split(AT_BOT)[1].strip().lower(), output['channel'], output
	return None, None, None

def send_message(channel_id, message):
	# channel_id can also be the form @username (all lowercase)
	slack_client.api_call(
		"chat.postMessage",
		channel=channel_id,
		text=message,
		username='hackthewest',
	)


if __name__ == "__main__":
	# print(slack_client.api_call("chat.postMessage", channel="", text="Not bad, not bad. Just making sure my brother Wes at the photobooth isn't in trouble...", as_user=True))

	# files = {'file': open('too_much_to_drink.jpg', 'rb')}
	# slack_client.api_call('files.upload', channels=["C2FMQ2291"], filename='Has anyone found my brother?!? I think he may have had too much to drink...', files=files)

    READ_WEBSOCKET_DELAY = 1 #1 sec delay b/w reading from firehose
    if slack_client.rtm_connect():
            print("StarterBot connected and running!")
            while True:
                    command, channel, message = parse_slack_output(slack_client.rtm_read())
                    if command and channel:
                            handle_command(command, channel, message)
                    time.sleep(READ_WEBSOCKET_DELAY)
    else:
            print("Connection failed. Invalid Slack token or bot ID?")
