#!/usr/local/bin/python3

import os, sys, json
import pandas as pd
from nltk.corpus import wordnet
import enchant

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
    price_num = 0
    if "http" in js["_jm_url"]:
        url = str(js["_jm_url"])
        domain = get_domain(url)
        if domain and "experiments" in js:
            price_num += 1
            for p in plist:
                for eid in js["experiments"]:
                    if p in str(js["experiments"][eid]):
                        auds = js["experiments"][eid]["audienceIds"]
                        if auds:
                            for a in auds:
                                if a.isdigit():
                                    price_f.write(domain + "\t" + p + "\t" + str(eid) + "\t" + str(a) + "\n")
                        else:
                            price_f.write(domain + "\t" + p + "\t" + str(eid) + "\t\n")
            """
            if price_num == 0:
                price_f.write(domain + "\t\n")
            """
    return True if price_num else False

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "optimizely_raw")
    price_path = os.path.join(file_path, "data", "optimizely_price.tsv")
    overview_path = os.path.join(file_path, "data", "optimizely_overview.tsv")
    
    plist = ["$", "sale", "price"]
    print(len(plist))

    # parse overview data
    #if not os.path.exists(price_path):
    if 1:
        price_f = open(price_path, "w")
        header = "domain\tprice\texperiment_id\taudience_id\n"
        price_f.write(header)
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
        price_f.close()

    df1 = pd.read_csv(overview_path, sep = "\t")
    df1 = df1.groupby("domain").sum()
    df1 = df1[df1["use_optimizely"] > 0]
    df1["domain"] = df1.index
    df2 = pd.read_csv(price_path, sep = "\t")
    #df2 = df2.drop_duplicates()
    df = df2.merge(df1, on = "domain")
    #df = df[["domain", "price"]].dropna()
    #df.to_csv(price_path, sep = "\t", index = False)
    print(df.groupby("domain").count())
