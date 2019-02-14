#!/usr/local/bin/python3

import os, sys, json
import pandas as pd

# parse a line
def parse(l):
    js = json.loads(l)
    print(js["audiences"]["7723861216"])
    #exit()
    if "experiments" in js.keys():
        for id in js["experiments"]:
            print(js["experiments"][id])

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    heritage_path = os.path.join(file_path, "data", "optimizely_raw", "heritage.txt")
    heritageaction_path = os.path.join(file_path, "data", "optimizely_raw", "heritageaction.txt")
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    experiment_path = os.path.join(file_path, "data", "optimizely_experiment.tsv")
    bias_path = os.path.join(file_path, "data", "twitter_share_score.csv")
    
    bias = pd.read_csv(bias_path)
    bias1 = bias[bias["domain"] == "heritage.org"]
    bias2 = bias[bias["domain"] == "heritageaction.com"]
    print(bias1, bias2)
    
    # parse overview data
    with open(heritage_path, "r") as f:
        l = f.readline()
        res = parse(l)
