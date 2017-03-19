#!/usr/bin/env python
#

import os
import csv

# Reads data about AMs in from .csv file, and returns it
# expects a .csv file named "am_data.csv" to be present in current directory
# and for file to have headers "twitter", "name" and "party"
def read_am_data():

    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "src_data")

    ams = []

    with open(os.path.join(data_dir, "am_data.csv"), "Ur") as am_file:
        reader = csv.DictReader(am_file)

        for line in reader:
            handle = line["twitter"].lstrip("@").strip()
            name = line["name"].strip()
            party = line["party"].strip()
            ams.append({"name": name, "twitter": handle, "party": party})

    return ams

def get_cache_filename(endpoint, aspect, params):

    file_string = "%s-%s-()-" % (endpoint, aspect)

    sorted_keys = sorted(params.keys())

    for k in sorted_keys:
        file_string += "-%s-%s" % (k, params[k])
    return file_string
