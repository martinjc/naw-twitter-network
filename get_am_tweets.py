#!/usr/bin/env python
#

import os
import sys
import csv
import json

from twitter_api import Twitter_API
from file_cache import JSONFileCache
from utils import *

def get_tweet_history(api, am):

    # make an api call to get the most recent tweets of the am
    params = {
        "screen_name": am,
        "count": 200,
        "exclude_replies": "false"
    }
    tweets = api.query_get("statuses", "user_timeline", params)

    # find the earliest tweet retrieved
    if len(tweets) > 0:
        earliest_id = tweets[0]["id"]
        for tweet in tweets:
            if tweet["id"] < earliest_id:
                earliest_id = tweet["id"]

        # assume there are more tweets to retrieve
        more_tweets = True

        # while there are more tweets to retrieve
        while(more_tweets):

            # make an api call to get the tweets prior
            # to our earliest retrieved tweet so far
            params = {
                "screen_name": am,
                "count": 200,
                "exclude_replies": "false",
                "max_id": earliest_id
            }

            new_tweets = ta.query_get("statuses", "user_timeline", params)

            # add the newly retrieved tweets to our list
            tweets.extend(new_tweets)

            # find the earliest retrieved tweet
            current_earliest = earliest_id
            for tweet in tweets:
                if tweet["id"] < earliest_id:
                    earliest_id = tweet["id"]

            # if the earliest tweet hasn't changed
            # we can't go back any further
            if current_earliest == earliest_id:
                more_tweets=False

    return tweets


def get_latest_tweets(api, am, tweets):

    # find the latest tweet retrieved
    latest_id = 0
    for tweet in tweets:
        if tweet["id"] > latest_id:
            latest_id = tweet["id"]

    # make a call and find the latest tweets
    params = {
        "screen_name": am,
        "count": 200,
        "exclude_replies": "false",
        "since_id": latest_id
    }
    new_tweets = api.query_get("statuses", "user_timeline", params)

    # add any new tweets to our set of tweets
    tweets.extend(new_tweets)
    # assume there's more
    more_tweets = True

    # find the latest tweet
    for tweet in tweets:
        if tweet["id"] > latest_id:
            latest_id = tweet["id"]

    while more_tweets:

        # make a call and find the latest tweets
        params = {
            "screen_name": am,
            "count": 200,
            "exclude_replies": "false",
            "since_id": latest_id
        }
        new_tweets = api.query_get("statuses", "user_timeline", params)

        # add any new tweets to our set of tweets

        for tweet in tweets: tweets.extend(new_tweets)

        current_latest = latest_id
        # find the latest tweet
        if tweet["id"] > latest_id:
            latest_id = tweet["id"]

        if current_latest == latest_id:
            more_tweets = False

    return tweets

def remove_duplicates(tweets):

    tweet_ids = []
    to_remove = []
    # go through all the tweets
    for tweet in tweets:
        # if we've already seen this tweet
        if tweet["id"] in tweet_ids:
            # add it to the list of tweets to remove
            to_remove.append(tweet)
        else:
            # otherwise add the ID to the list of tweets we've seen
            tweet_ids.append(tweet["id"])

    for tweet in to_remove:
        tweets.remove(tweet)

    return tweets


if __name__ == "__main__":

    # load the AM data from the csv
    am_data = read_am_data()

    # construct a list of all those AMs with Twitter accounts
    am_twitter_list = sorted([am["twitter"] for am in am_data if am["twitter"] is not ""])

    print(am_twitter_list)

    cache = JSONFileCache()
    ta = Twitter_API()

    for am in am_twitter_list:

        print(am)

        # get the list of tweets that have been downloaded, if it exists
        am_cache_file = "%s_tweets.json" % (am)

        if cache.file_exists(am_cache_file):
            tweets = cache.get_json(am_cache_file)
        else:
            tweets = []

        print(len(tweets))

        if len(tweets) > 0:
            tweets = get_latest_tweets(ta, am, tweets)
        else:
            tweets = get_tweet_history(ta, am)

        print(len(tweets))

        tweets = remove_duplicates(tweets)

        print(len(tweets))

        cache.put_json(tweets, am_cache_file)
