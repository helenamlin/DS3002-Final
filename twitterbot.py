# Ruth Efrem and Helena Lindsey
# Twitter Account Handle: @ds3002bot
import tweepy
import time
import requests
import json

auth = tweepy.OAuthHandler("qNqHyZddvOMKSi1cyZKPhB8pW", "gEGf3KIVhFOFRml2MnVdIlNhnqKtiPaSted4Fd7I0PlV322U2q")
auth.set_access_token("1521283232091807745-4vLuFxo4ciPCYBRGz3fYD7OVgHBCQ8",
                      "8dSTMPcg5Gx4BvqfEJXGR3VfUMM7qWAbcwmg6hI8UxKS8")

# provides access to Twitter API and connects @ds3002bot to python

api = tweepy.API(auth)
# allows bot to tweet, retweet, like, etc.

# api.update_status("This is my tweet") --> practice/test tweet from pycharm

response_API = requests.get('https://api.kanye.rest/')
# print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)

# retrieves data from an api that generates random Kanye West quotes


FILE_NAME = 'last_seen.txt'


# used to store the id of tweets that mention @ds3002bot


def read_last_seen(file_name):
    file_read = open(file_name, 'r')
    last_seen_id = file_read.read().strip()
    # does that need an int()^?
    file_read.close()
    return last_seen_id


# opening file, specifying r for read, reading value inside of file and assigning it to new variable, closing file,
# and returning the last seen ID

def store_last_seen(last_seen_id, file_name):
    file_write = open(file_name, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


# opening file when specifying w for write, then write last seen id of the tweet, closing file and returning

# All together, these functions are supposed to make it so the bot does not reply to a tweet it has already
# seen/replied


def reply():
    last_seen_id = read_last_seen(FILE_NAME)
    tweets = api.mentions_timeline(count=last_seen_id, tweet_mode='extended')
    for tweet in reversed(tweets):
        last_seen_id = tweet.id
        store_last_seen(last_seen_id, FILE_NAME)
        # stores the ID of each tweet, so it is not replied to more than once
        if '#helloworld' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status(status="@" + tweet.user.screen_name + " Hello world to you too!",
                              in_reply_to_status_id=tweet.id)

        if '#mentalhealthhelp' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status(
                status="@" + tweet.user.screen_name + " Use this link for access to mental health resources: "
                                                      "https://www.mentalhealth.gov/get-help/immediate-help",
                in_reply_to_status_id=tweet.id)

        if '#kanyequote' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status(status="@" + tweet.user.screen_name + " Here's a Kanye Quote! : " + data,
                              in_reply_to_status_id=tweet.id)

        if '#help' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status(
                status="@" + tweet.user.screen_name + " I can greet you with #helloworld, give you access to mental "
                                                      "health resources with #mentalhealthhelp, and tell you the best "
                                                      "Kanye quotes with #kanyequote",
                in_reply_to_status_id=tweet.id)


# Referring to the if statements: for each tweet with the specific hashtags mentioned above, it is returning the ID,
# full text, and responding to the tweet with the specific response designed and given above

while True:
    reply()
    time.sleep(15)

# Makes it so the bot auto replies to any tweet that is tweeted at the bot with the appropriate hashtag within 15 sec
