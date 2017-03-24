#!/usr/bin/env python
#

import os
import sys
import csv
import json

from file_cache import JSONFileCache
from utils import *

def get_colour(am):
    if am["party"] == "Labour":
        return "#dc241f"
    elif am["party"] == "Conservative":
        return "#0087DC"
    elif am["party"] == "Liberal Democrat":
        return "#fdbb30"
    elif am["party"] == "Plaid Cymru":
        return "#008142"
    elif am["party"] == "UKIP":
        return "#70147a"
    elif am["party"] == "Independent":
        return "#eeeeee"
    else:
        return None


def construct_mention_matrix():
    # load the AM data from the csv
    am_data = read_am_data()

    # construct a list of all those AMs with Twitter accounts
    am_twitter_list = sorted([am["twitter"] for am in am_data if am["twitter"] is not ""])

    # matrix of mentions
    mention_matrix = {}
    for am in am_twitter_list:
        mention_matrix[am] = {}
        for other_am in am_twitter_list:
            mention_matrix[am][other_am] = 0

    cache = JSONFileCache()

    for am in am_twitter_list:

        # get the list of tweets that have been downloaded, if it exists
        am_cache_file = "%s_tweets.json" % (am)
        if cache.file_exists(am_cache_file):
            tweets = cache.get_json(am_cache_file)

            for tweet in tweets:
                for mention in tweet["entities"]["user_mentions"]:
                    if mention["screen_name"] in am_twitter_list:
                        mention_matrix[am][mention["screen_name"]] += 1

    return mention_matrix



if __name__ == "__main__":

    am_data = read_am_data()
    am_parties = {}
    for am in am_data:
        am_parties[am["twitter"]] = am["party"]

    mention_matrix = construct_mention_matrix()

    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data")
    with open(os.path.join(data_dir, "mention_matrix.csv"), "w") as output_file:

        for am in sorted(mention_matrix.keys()):
            output_file.write(",%s" % am)
        output_file.write("\n")

        for am in sorted(mention_matrix.keys()):
            output_file.write("%s" % am)
            for other_am in sorted(mention_matrix.keys()):
                output_file.write(",%d" % mention_matrix[am][other_am])
            output_file.write("\n")

    with open(os.path.join(data_dir, "mention_list.csv"), "w") as output_file:

        output_file.write("am1,am2,mentions,party\n");
        for am1 in sorted(mention_matrix.keys()):
            for am2 in sorted(mention_matrix.keys()):
                if am1 != am2 and mention_matrix[am1][am2] != 0:
                    output_file.write("%s,%s,%d,%s\n" % (am1, am2, mention_matrix[am1][am2], am_parties[am1]))


    data = {"nodes": [], "links": []}
    for am in am_data:
        data["nodes"].append({
            "id": am["twitter"],
            "name": am["name"],
            "twitter": am["twitter"],
            "party": am["party"],
            "colour": get_colour(am)
        })

    for am1 in sorted(mention_matrix.keys()):
        for am2 in sorted(mention_matrix.keys()):
            if mention_matrix[am1][am2] >= 5 and am1 != am2:
                data["links"].append({
                    "source": am1,
                    "target": am2,
                    "value": mention_matrix[am1][am2]
                    })


    with open(os.path.join(data_dir, "mention_network.json"), "w") as output_file:
        json.dump(data, output_file)
