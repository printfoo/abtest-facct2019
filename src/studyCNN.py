#!/usr/local/bin/python3

import os, sys, json
import pandas as pd

# parse a line
def parse(l):
    js = json.loads(l)
    if "experiments" in js.keys():
        for id in js["experiments"]:
            if "Taboola" in js["experiments"][id]["name"] or "Outbrain" in js["experiments"][id]["name"]:
                print(json.dumps(js["experiments"][id], indent=4))

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    study_domain = "cnn.com"
    domain_path = os.path.join(file_path, "data", "optimizely_raw", study_domain.split(".")[0] + ".txt")
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    experiment_path = os.path.join(file_path, "data", "optimizely_experiment.tsv")
    
    audience = pd.read_csv(audience_path, sep = "\t")
    audience = audience[audience["domain"] == study_domain]["audience_id"].drop_duplicates()
    print(len(audience))
    
    experiment = pd.read_csv(experiment_path, sep = "\t")
    experiment = experiment[experiment["domain"] == study_domain]["experiment_id"].drop_duplicates()
    print(len(experiment))
    exit()
    
    # parse overview data
    with open(domain_path, "r") as f:
        l = f.readline()
        res = parse(l)
