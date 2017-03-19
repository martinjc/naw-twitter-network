#!/usr/bin/env python
#


import json

from itertools import combinations

from file_cache import JSONFileCache
from twitter_api import Twitter_API
from utils import *


if __name__ == "__main__":

    # read in the AM data
    am_data = read_am_data()
    print(am_data)

    # construct a list of all those AMs with Twitter accounts
    am_twitter_list = sorted([am["twitter"] for am in am_data if am["twitter"] is not ""])

    # cache for caching Twitter response
    cache = JSONFileCache()

    # API object for accessing Twitter API
    ta = Twitter_API()

    # find all pairs of AMs
    combos = combinations(am_twitter_list, 2)

    count = 0

    # for each combination
    for combo in combos:
        am1 = combo[0]
        am2 = combo[1]

        # make a request to see if the AMs follow each other
        params = {
            "source_screen_name": am1,
            "target_screen_name": am2
        }

        friendship_filename = get_cache_filename("friendships", "show", params)

        # use the result from the cache if it exists, otherwise call Twitter API
        if not cache.file_exists(friendship_filename):
            friendship = ta.query_get("friendships", "show", params)
            cache.put_json(friendship, friendship_filename)
        else:
            friendship = cache.get_json(friendship_filename)

        # do some output to show results and progress
        am1_follows_am2 = friendship["relationship"]["source"]["following"]
        am2_follows_am1 = friendship["relationship"]["target"]["following"]

        count += 1
        print("%d" % (count))
        if am1_follows_am2 and am2_follows_am1:
            print("%s and %s follow each other" % (am1, am2))
        else:
            print("%s and %s do not follow each other" % (am1, am2))
