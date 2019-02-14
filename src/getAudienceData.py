#!/usr/local/bin/python3

import os, sys, json
import pandas as pd

# get all conditions from condition list
def get_conditions(list, domain, crawl_time, audience_id, audience_name):
    for component in list:
        if type(component) == type([]):
            get_conditions(component, domain, crawl_time, audience_id, audience_name)
        elif type(component) == type({0:0}):
            cond_match = component["match"]
            cond_name = component["name"]
            cond_type = component["type"]
            cond_value = component["value"].encode("unicode_escape").decode()
            save_str = domain + "\t" + crawl_time + "\t" + audience_id + "\t" + audience_name + "\t" + \
                cond_match + "\t" + cond_name + "\t" + cond_type + "\t" + cond_value + "\n"
            audience_f.write(save_str)

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
    audience_num = 0
    if "http" in js["_jm_url"]:
        url = str(js["_jm_url"])
        domain = get_domain(url)
        if domain:
            crawl_time = str(js["_jm_time"] - js["_jm_time"] % (60 * 60 * 1000))
            if "audiences" in js.keys():
                for audience_id in js["audiences"].keys():
                    audience_name = js["audiences"][audience_id]["name"]
                    audience_conditions_list = js["audiences"][audience_id]["conditions"]
                    audience_conditions = get_conditions(audience_conditions_list,
                                                         domain, crawl_time, audience_id, audience_name)
                    audience_num += 1
    return True if audience_num else False

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "optimizely_raw")
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    
    # parse overview data
    #if not os.path.exists(audience_path):
    if 1:
        audience_f = open(audience_path, "w")
        header = "domain\tcrawl_time\taudience_id\taudience_name\tcond_match\tcond_name\tcond_type\tcond_value\n"
        audience_f.write(header)
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
        audience_f.close()
