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
import networkx as nx
import matplotlib.pyplot as plt

from itertools import combinations
from networkx.readwrite import json_graph

from construct_follow_matrix import construct_follow_matrix
from construct_mention_matrix import construct_mention_matrix
from utils import *


def output_graph(G, file_path):
    json_data = json_graph.node_link_data(G)
    json.dump(json_data, file_path)


def add_nodes(am_data, G):
    for i, am in enumerate(am_data):
        if am["party"] == "Labour":
            colour = "#dc241f"
        elif am["party"] == "Conservative":
            colour = "#0087DC"
        elif am["party"] == "Liberal Democrat":
            colour = "#fdbb30"
        elif am["party"] == "Plaid Cymru":
            colour = "#008142"
        elif am["party"] == "UKIP":
            colour = "#70147a"
        elif am["party"] == "Independent":
            colour = "#eeeeee"
        else:
            print(am)

        G.add_node(am["twitter"], name=am["name"], twitter=am["twitter"], party=am["party"], colour=colour)
    return G


def construct_mutual_follow_graph(am_data, follows):

    G = nx.Graph()

    G = add_nodes(am_data, G)

    for am1 in sorted(follows.keys()):
        for am2 in sorted(follows.keys()):
            if follows[am1][am2] == 1 and follows[am2][am1] == 1:
                G.add_edge(am1, am2)

    return G


if __name__ == "__main__":

    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data")
    graph_dir = os.path.join(cwd, "graphs")

    # read in the AM data
    am_data = read_am_data()

    mentions_matrix = construct_mention_matrix()
    follow_matrix = construct_follow_matrix()

    graph = construct_mutual_follow_graph(am_data, follow_matrix)

    with open(os.path.join(graph_dir, "mutual_follow_graph.gml"), "w") as gml_file:
        nx.write_graphml(graph, gml_file)

    with open(os.path.join(graph_dir, "mutual_follow_graph.json"), "w") as json_file:
        output_graph(graph, json_file)
