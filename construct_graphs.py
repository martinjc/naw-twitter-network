#!/usr/bin/env python
#
# Copyright 2014 Martin J Chorley
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import json
from itertools import combinations

from construct_follow_matrix import construct_follow_matrix
from construct_mention_matrix import construct_mention_matrix
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


def construct_mutual_follow_json_d3(am_data, follows):

    data = {"nodes": [], "links": []}
    for am in am_data:
        data["nodes"].append({
            "id": am["twitter"],
            "name": am["name"],
            "twitter": am["twitter"],
            "party": am["party"],
            "colour": get_colour(am)
        })
    complete = [];
    for am1 in sorted(follows.keys()):
        for am2 in sorted(follows.keys()):
            if am2 not in complete:
                if follows[am1][am2] == 1 and follows[am2][am1] == 1:
                    data["links"].append({
                        "source": am1,
                        "target": am2
                    })
        complete.append(am1)

    return data

def construct_follow_json_d3(am_data, follows):

    data = {"nodes": [], "links": []}
    for am in am_data:
        data["nodes"].append({
            "id": am["twitter"],
            "name": am["name"],
            "twitter": am["twitter"],
            "party": am["party"],
            "colour": get_colour(am)
        })
    for am1 in sorted(follows.keys()):
        for am2 in sorted(follows.keys()):
            if follows[am1][am2] == 1:
                data["links"].append({
                    "source": am1,
                    "target": am2
                })

    return data

if __name__ == "__main__":

    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data")
    graph_dir = os.path.join(cwd, "graphs")

    # read in the AM data
    am_data = read_am_data()

    #mentions_matrix = construct_mention_matrix()
    follow_matrix = construct_follow_matrix()

    d3_json = construct_follow_json_d3(am_data, follow_matrix)

    with open(os.path.join(graph_dir, "follow_graph_d3.json"), "w") as json_file:
        json.dump(d3_json, json_file)
