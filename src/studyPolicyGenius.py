#!/usr/local/bin/python3

import os, sys, json
import pandas as pd

# parse a line
def parse(l):
    js = json.loads(l)
    print(js["experiments"]["10292800034"]) # 29.9
    print(js["audiences"]["10258136020"])
    
    print(js["experiments"]["10246545333"]) # 10
    print(js["audiences"]["10197320704"])
    
    print(js["experiments"]["10300180005"]) # 9.9
    print(js["audiences"]["10279323027"])

    """
    if "experiments" in js.keys():
        for id in js["experiments"]:
            for v_id in js["experiments"][id]["variations"]:
                print(json.dumps(js["experiments"][id], indent=4))
    """

    #https://www.policygenius.com/life-insurance/compare-and-apply
    #https://www.policygenius.com/life-insurance/compare-and-save-40

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    study_domain = "policygenius.com"
    domain_path = os.path.join(file_path, "data", "optimizely_raw", study_domain.split(".")[0] + ".txt")
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    experiment_path = os.path.join(file_path, "data", "optimizely_experiment.tsv")
    
    audience = pd.read_csv(audience_path, sep = "\t")
    audience = audience[audience["domain"] == study_domain]["audience_id"].drop_duplicates()
    print(len(audience))
    
    experiment = pd.read_csv(experiment_path, sep = "\t")
    experiment = experiment[experiment["domain"] == study_domain]["experiment_id"].drop_duplicates()
    print(len(experiment))
    
    # parse overview data
    with open(domain_path, "r") as f:
        l = f.readline()
        res = parse(l)
