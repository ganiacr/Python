import tweepy
from time import sleep
from credentials import *
from config import QUERY, FOLLOW, LIKE, SLEEP_TIME
import time


client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

print("Twitter bot which retweets, like tweets and follow users")
print("Bot Settings")
print("Like Tweets :", LIKE)
print("Follow users :", FOLLOW)

QUERY = "example"

backoff = 1  # initial backoff in seconds

for tweet in tweepy.Paginator(
        client.search_recent_tweets,
        query=QUERY,
        tweet_fields=['author_id'],
        expansions=['author_id'],
        max_results=10
    ).flatten(limit=100):

    print(tweet)
    try:
        # Get user info
        user_id = tweet.author_id
        user = client.get_user(id=user_id).data
        print('\nTweet by: @' + user.username)

        # Retweet
        client.retweet(tweet.id)
        print('Retweeted the tweet')
        sleep(SLEEP_TIME)

        # Like
        if LIKE:
            client.like(tweet.id)
            print('Favorited the tweet')
            sleep(SLEEP_TIME)

        # Follow
        if FOLLOW:
            client.follow_user(user_id)
            print('Followed the user')
            sleep(SLEEP_TIME)

        backoff = 1  # reset backoff after success

    except tweepy.TooManyRequests:
        print(f"Rate limit reached. Sleeping for {backoff} seconds...")
        time.sleep(backoff)
        backoff = min(backoff * 2, 900)  # max 15 minutes
    except tweepy.TweepyException as e:
        print(e)

