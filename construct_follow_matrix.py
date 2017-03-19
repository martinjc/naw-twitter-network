#!/usr/bin/env python
#

import os
import json

from itertools import combinations

from file_cache import JSONFileCache
from twitter_api import Twitter_API
from utils import *


def construct_follow_matrix():

    # read in the AM data
    am_data = read_am_data()

    # construct a list of all those AMs with Twitter accounts
    am_twitter_list = sorted([am["twitter"] for am in am_data if am["twitter"] is not ""])

    # cache for caching Twitter response
    cache = JSONFileCache()

    # API object for accessing Twitter API
    ta = Twitter_API()

    # matrix of following/not-following
    follow_matrix = {}
    for am in am_twitter_list:
        follow_matrix[am] = {}
        for other_am in am_twitter_list:
            follow_matrix[am][other_am] = 0

    # find all pairs of AMs
    combos = combinations(am_twitter_list, 2)

    count = 0
    for combo in combos:
        am1 = combo[0]
        am2 = combo[1]

        params = {
            "source_screen_name": am1,
            "target_screen_name": am2
        }

        friendship_filename = get_cache_filename("friendships", "show", params)

        if not cache.file_exists(friendship_filename):
            friendship = ta.query_get("friendships", "show", params)
            cache.put_json(friendship, friendship_filename)
        else:
            friendship = cache.get_json(friendship_filename)

        am1_follows_am2 = friendship["relationship"]["source"]["following"]
        am2_follows_am1 = friendship["relationship"]["target"]["following"]

        if am1_follows_am2:
            follow_matrix[am1][am2] = 1
        if am2_follows_am1:
            follow_matrix[am2][am1] = 1

    return follow_matrix



if __name__ == "__main__":


    follow_matrix = construct_follow_matrix()

    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data")
    with open(os.path.join(data_dir, "follow_matrix.csv"), "w") as follow_file:

        for am in sorted(follow_matrix.keys()):
            follow_file.write(",%s" % am)
        follow_file.write("\n")

        for am in sorted(follow_matrix.keys()):
            follow_file.write("%s" % am)
            for other_am in sorted(follow_matrix.keys()):
                follow_file.write(",%d" % follow_matrix[am][other_am])
            follow_file.write("\n")
