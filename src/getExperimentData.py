#!/usr/local/bin/python3

import os, sys, json
import pandas as pd

# get domain from url
def get_domain(url):
    web = url.split("/")[2] # www.something.postfix
    if name[:-4] in web.split("."): # if something == file_name
        post_fix = web.split(name[:-4])[-1]
        return name[:-4] + post_fix
    else:
        return None

# parse a line
def parse(l):
    js = json.loads(l)
    experiment_num = 0
    if "http" in js["_jm_url"]:
        url = str(js["_jm_url"])
        domain = get_domain(url)
        if domain:
            crawl_time = str(js["_jm_time"] - js["_jm_time"] % (60 * 60 * 1000))
            if "experiments" in js.keys():
                for experiment_id in js["experiments"].keys():
                    if js["experiments"][experiment_id]:
                        audiences = js["experiments"][experiment_id]["audienceIds"]
                        audiences = [a for a in audiences if type(a) != type([])]
                        audiences = [a for a in audiences if a not in {"and", "or", "not"}]
                        audience_num = str(len(audiences))
                        audience_name = js["experiments"][experiment_id]["audienceName"]
                        experiment_name = js["experiments"][experiment_id]["name"].replace("\t", " ")
                        variations = js["experiments"][experiment_id]["variations"] # dig deeper in the future
                        """
                        for v in variations:
                            if len(v["actions"]) > 0:
                                if len(v["actions"][0]["changes"]) > 0:
                                    if "type" in v["actions"][0]["changes"][0].keys():
                                        print(v["actions"][0]["changes"][0]["type"])
                        """
                        variations_num = str(len(variations))
                        save_str = domain + "\t" + crawl_time + "\t" + experiment_id + "\t" + experiment_name + "\t" + \
                            audience_num + "\t" + audience_name + "\t" + variations_num + "\n"
                        experiment_f.write(save_str)
                        experiment_num += 1
    return True if experiment_num else False

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "optimizely_raw")
    experiment_path = os.path.join(file_path, "data", "optimizely_experiment.tsv")
    
    # parse overview data
    #if not os.path.exists(audience_path):
    if 1:
        experiment_f = open(experiment_path, "w")
        header = "domain\tcrawl_time\texperiment_id\texperiment_name\taudience_num\taudience_name\tvariation_num\n"
        experiment_f.write(header)
        for _, _, names in os.walk(raw_path):
            for name in names:
                with open(os.path.join(raw_path, name), "r") as f:
                    while True:
                        l = f.readline()
                        if not l:
                            break
                        res = parse(l)
                        if res:
                            break
        experiment_f.close()
