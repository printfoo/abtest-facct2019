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
    if "http" in js["_jm_url"]:
        url = str(js["_jm_url"])
        print(url)
        domain = get_domain(url)
        if domain:
            crawl_time = str(js["_jm_time"] - js["_jm_time"] % (24 * 60 * 60 * 1000))
            if "accountId" in js.keys():
                overview_f.write(domain + "\t" + url + "\t" + crawl_time + "\t1\t1\n")
            else:
                overview_f.write(domain + "\t" + url + "\t" + crawl_time + "\t1\t0\n")

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "optimizely_raw")
    overview_path = os.path.join(file_path, "data", "optimizely_overview.tsv")
    domain_rank_path = os.path.join(file_path, "data", "optimizely_domain_rank.csv")
    alexa_path = os.path.join(file_path, "data", "alexa_top1m.csv")
    
    # parse overview data
    #if not os.path.exists(overview_path):
    if 1:
        overview_f = open(overview_path, "w")
        overview_f.write("domain\turl\tcrawl_time\tcrawl_count\tuse_optimizely\n")
        for _, _, names in os.walk(raw_path):
            for name in names:
                with open(os.path.join(raw_path, name), "r") as f:
                    while True:
                        l = f.readline()
                        if not l:
                            break
                        parse(l)
        overview_f.close()

    # join data with alexa top 1m
    else:
        alexa = pd.read_csv(alexa_path, names = ["rank", "domain"])
        df = pd.read_csv(overview_path, sep = "\t")
        df = df.groupby("domain").sum()
        df["domain"] = df.index
        df = df.merge(alexa, on = "domain")
        df[["domain", "crawl_count", "use_optimizely", "rank"]] \
            .to_csv(domain_rank_path, index = False)
