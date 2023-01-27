import requests
import tweepy
import argparse

from helpers import *

from urllib3.exceptions import ProtocolError
from socket import timeout
from requests.exceptions import HTTPError

EXCEPTIONS = [HTTPError,
              TimeoutError,
              timeout,
              ConnectionResetError,
              ProtocolError]

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-config', '--config_path',
                    type=str,
                    required=True)

args = parser.parse_args()

# Load auth configs
CONFIG_PATH = args.config_path
config_dict = load_json(CONFIG_PATH)

TELEGRAM_BOT_TOKEN = config_dict['telegram']['bot_token']
TELEGRAM_CHAT_ID = config_dict['telegram']['chat_id']

TWITTER_CONSUMER_KEY = config_dict['twitter']['consumer_key']
TWITTER_CONSUMER_SECRET = config_dict['twitter']['consumer_secret']
TWITTER_ACCESS_TOKEN = config_dict['twitter']['access_token']
TWITTER_ACCESS_TOKEN_SECRET = config_dict['twitter']['access_token_secret']

# Instantiate Telegram and Twitter tweepy_api objects
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN,
                      TWITTER_ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth)

binance_handle_list = ['binance']
# We can only listen to twitter users by ID (primary key), not handle, so we get the IDs first
user_objects = tweepy_api.lookup_users(screen_names=binance_handle_list)
binance_user_id_list = [user_objects[0].id]


def listing_handler(handle, text):
    print('Sending message to telegram chat')
    text = f'Binance listing detected! Tweet content: {text}'
    send_text = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + TELEGRAM_CHAT_ID + '&word_list=' + text
    response = requests.get(send_text)

    # Send trading orders...


def is_tweet_binance_listing(handle, text):
    if 'binance' in handle and 'will list' in text.lower():
        return True

class StreamListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__(api=tweepy_api)

    def on_status(self, status: tweepy.models.Status):
        if status.user.screen_name in binance_handle_list:
            handle = status.user.screen_name
            text = status.text
            if listing_handler(handle, text) is True:
                print('Binance listing detected!')
                listing_handler(handle, text)


if __name__ == '__main__':

    @keep_trying(EXCEPTIONS)
    def runListener():
        myStreamListener = StreamListener()
        myStream = tweepy.Stream(auth=tweepy_api.auth, listener=myStreamListener)
        myStream.filter(follow=binance_user_id_list)

    runListener()
