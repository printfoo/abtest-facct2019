#!/usr/local/bin/python3

import os, sys, json
import pandas as pd

# parse a line
def parse(l):
    js = json.loads(l)
    print(js["audiences"]["9861004187"])

    if "campaigns" in js.keys():
        for id in js["campaigns"]:
            print(js["campaigns"][id]["name"])
            if js["campaigns"][id]["name"] == "EXO - B2B Personalization Headers":
                for x in js["campaigns"][id]["experiments"]:
                    print(x["name"])
                #print(json.dumps(js["campaigns"][id]["experiments"]["name"], indent=4))

    if "experiments" in js.keys():
        for id in js["experiments"]:
            for v_id in js["experiments"][id]["variations"]:
                if v_id["id"] == "9909598216":
                    print(json.dumps(js["experiments"][id], indent=4))
                    break
    exit()

    if "audiences" in js.keys():
        for id in js["audiences"]:
            if id in ["6992450319", "9030630106", "7209740780"]:
                print(json.dumps(js["audiences"][id], indent=4))

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    nytimes_path = os.path.join(file_path, "data", "optimizely_raw", "nytimes.txt")
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    experiment_path = os.path.join(file_path, "data", "optimizely_experiment.tsv")
    bias_path = os.path.join(file_path, "data", "twitter_share_score.csv")
    
    audience = pd.read_csv(audience_path, sep = "\t")
    audience = audience[audience["domain"] == "nytimes.com"]["audience_name"].drop_duplicates()
    print(len(audience))
    
    experiment = pd.read_csv(experiment_path, sep = "\t")
    experiment = experiment[experiment["domain"] == "nytimes.com"]["experiment_name"].drop_duplicates()
    print(len(experiment))
    
    bias = pd.read_csv(bias_path)
    bias = bias[bias["domain"] == "nytimes.com"]
    print(bias)
    
    # parse overview data
    with open(nytimes_path, "r") as f:
        l = f.readline()
        res = parse(l)
