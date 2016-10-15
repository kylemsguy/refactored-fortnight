import os
from slackclient import SlackClient

USER_NAME = 'amy'

slack_client = SlackClient(os.environ.get("SLACK_TOKEN"))

def find_slack_names(user_name):
	api_call = slack_client.api_call("users.list")
	if api_call.get('ok'):
		user_dict = {}
		# retrieve all users so we can find our bot
		users = api_call.get('members')
		for user in users:
			if 'real_name' in user and user.get('real_name').lower().startswith(USER_NAME.lower()):
				user_dict[user.get('real_name')] = user.get('id')
		return user_dict
	else:
		print("Error connecting to slack api")
		return None

def find_slack_username(user_id):
	api_call = slack_client.api_call("users.list")
	if api_call.get('ok'):
		users = api_call.get('members')
		for user in users:
			if 'id' in user and user_id == user.get('id'):
				if 'name' in user:
					return user.get('name')
				else:
					print("Error couldn't find username for user id: " + user_id)
					return None
	else:
		print("Error connecting to slack api")
		return None

if __name__ == "__main__":
        print(find_slack_names(USER_NAME))
	# TODO: None check this
	username = find_slack_username("U2PP30M33")
	if username is None:
		print("Couldn't find username based on id")
	else:

		print("Bot username based on id: " + username)
