import os
import time
import re
from random import randint
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"
SECONDS_TO_MESSAGE = 3 # 3600   # 1 hour
HOURS_IN_HACKATHON = 36 
THREE_CLASSES = ["front end developer", "back end developer", "designer"]

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

# player progess and info
player_stages = {}
message_timers = {}
player_type = None  # String from THREE_CLASSES
player_scores = {}  # front(0), back(1), design(2)
player_roadblocks = {}

def handle_command(command, channel):
    """
        gets commands directed at bot, determines if valid. 
        if so then acts on commands
        if not returns whats needed for clarification
    """
    if channel not in player_stages:
        player_stages[channel] = "unstarted"

    stage = player_stages[channel]
    input = command.lower()
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers, delimited by spaces."

    if input.startswith(EXAMPLE_COMMAND):
        response = "Do what?"
    elif input.startswith("status"):
        if (stage == "unstarted"):
            response = "You need to start a game first! Type 'join game' to do so."
        else:
            # TODO: return status
            pass


    elif stage == "unstarted" and input.startswith("join game"):
        response = "Created new game! Tell me, are you a front end developer, back end developer, or designer?"
        player_stages[channel] = "choose_position"
        ## do server stuff here
    elif stage == "choose_position":
        if re.match("front ?end.*", input):
            response = "You've chosen front end developer!"
            player_type = "front_end"
        elif re.match("back ?end.*", input):
            response = "You've chosen back end developer!"
            player_type = "back_end"
        elif re.match("design.*", input):
            response = "You've chosen designer!"
            player_type = "designer"
        else:
            response = "That's not a valid response. You must be a designer!"
            player_type = "designer"

        player_stages[channel] = "type_chosen"
        message_timers[channel] = 0 # start the timer
        response = response + " Progress will continue slowly as time goes by, type 'status' to check in. " + \
                "Occasionally you'll come across a roadblock with your hack, " + \
                "you'll need to network with the hackers around you to overcome these problems."
    elif stage == "type_chosen" and input.startswith("link"):
        pass

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


def increment_timer():
    """
        called each second to increment timer for all players
        if it exceeds SECONDS_TO_MESSAGE we randomly generate a role and send out a message
    """

    for timer_key in message_timers:
        if player_stages[timer_key] == "unstarted" or player_stages[timer_key] == "choose_positions":
            # don't increment
            pass
        else:
            # increment
            message_timers[timer_key] = message_timers[timer_key] + 1
            # check
            if message_timers[timer_key] >= SECONDS_TO_MESSAGE:
                # reset
                message_timers[timer_key] = 0
                # select roadblock of the three
                role = THREE_CLASSES[randint(0,2)]
                # TODO: block progress
                
                # send out response
                response = "Roadblock! Find a " + role + " to continue progress on your hack!" + \
                            " When you've met up with them, get them to use the command 'link @<yournamehere>' with me to resume progress."
                send_message(timer_key, response)
            # increment score once a second
            

### TODO: Make link command, limit to one per person.
### TODO: validate their position
### TODO: channel -> user?
### TODO: increment score
### TODO: convert score to percentage
### TODO: status command
            

if __name__ == "__main__":
        READ_WEBSOCKET_DELAY = 1 #1 sec delay b/w reading from firehose
        

        if slack_client.rtm_connect():
                print("StarterBot connected and running!")
                while True:
                        command, channel = parse_slack_output(slack_client.rtm_read())
                        if command and channel:
                                handle_command(command, channel)
                        increment_timer()
                        time.sleep(READ_WEBSOCKET_DELAY)
        else:
                print("Connection failed. Invalid Slack token or bot ID?")
