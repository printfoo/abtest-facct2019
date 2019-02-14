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
    ad_num = 0
    if "http" in js["_jm_url"]:
        url = str(js["_jm_url"])
        domain = get_domain(url)
        if domain:
            js_str = l.lower()
            for ad in adlist:
                if ad in js_str:
                    ad_f.write(domain + "\t" + ad + "\n")
                    ad_num += 1
            if ad_num == 0:
                ad_f.write(domain + "\t\n")
    return True if ad_num else False

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    raw_path = os.path.join(file_path, "data", "optimizely_raw")
    ad_web_path = os.path.join(file_path, "data", "filtered_tracker_or_ads.txt")
    ad_path = os.path.join(file_path, "data", "optimizely_advertisement.tsv")
    overview_path = os.path.join(file_path, "data", "optimizely_overview.tsv")
    
    d = enchant.Dict("en_US")
    with open(ad_web_path) as ad_web_f:
        adlist = ad_web_f.read().strip("\n").split("\n")
    adlist = [a for a in adlist if not d.check(a) and len(a) > 3 and a not in {"optimizely", "lytics", "estat", "microsoft", "paypal", "affec", "youtube", "simpli", "adap", "pinterest", "ebay", "cleveland"}]
    print(len(adlist))

    # parse overview data
    #if not os.path.exists(audience_path):
    if 1:
        ad_f = open(ad_path, "w")
        header = "domain\tadvertisement\n"
        ad_f.write(header)
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
        ad_f.close()

    df1 = pd.read_csv(overview_path, sep = "\t")
    df1 = df1.groupby("domain").sum()
    df1 = df1[df1["use_optimizely"] > 0]
    df1["domain"] = df1.index
    df2 = pd.read_csv(ad_path, sep = "\t")
    df2 = df2.drop_duplicates()
    df = df2.merge(df1, on = "domain")
    df = df[["domain", "advertisement"]].dropna()
    df.to_csv(ad_path, sep = "\t", index = False)
    print(df.groupby("advertisement").count())
