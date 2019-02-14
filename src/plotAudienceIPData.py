#!/usr/local/bin/python3

import os, sys, json
import numpy as np
import pandas as pd
import ipaddress
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from scipy.stats import spearmanr, pearsonr
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.size"] = 8
font = FontProperties()
font.set_size(8)
font2 = FontProperties()
font2.set_size(8)
font2.set_weight("bold")
font3 = FontProperties()
font3.set_size(7)

# get label from string
def get_label(x):
    x = x.split("_")[0]
    return x.upper() if len(x) <= 2 else x.capitalize()

# get ip 32 from string
def get_ip(x):
    try:
        x = int(ipaddress.IPv4Address(x))
    except:
        x = np.nan
    return x

# get as from ip 32
def get_as(ip):
    tmp = ip2as[ip2as["min"] < ip]
    tmp = tmp[tmp["max"] > ip]
    tmp = tmp[tmp["asn"] != 0]
    return tmp["asn"].values[0]

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    ip2as_path = os.path.join(file_path, "data", "ip2asn-v4-u32.tsv")
    fig_path = os.path.join(file_path, "results", "audience_ip_distribution.pdf")
    
    # read and plot
    df = pd.read_csv(audience_path, sep = "\t")
    sel_types = {"browser_version", "cookies", "device", "ip", "location", "platform", "language"}
    df["type"] = df["cond_type"].apply(lambda x: x if x in sel_types else "customized")
    df["type"] = df["type"].apply(lambda x: get_label(x))
    tdf = df[df["type"] == "IP"]
    tdf["ip"] = tdf["cond_value"].apply(get_ip)
    tdf = tdf.dropna(subset = {"ip"})
    print(len(tdf))
    ip2as = pd.read_csv(ip2as_path, sep = "\t", names = ["min", "max", "asn", "country", "info"])
    tdf["asn"] = tdf["ip"].apply(get_as)
    ip2as = ip2as[["asn", "country", "info"]].drop_duplicates()
    tdf = tdf.merge(ip2as, on = "asn")
    country_ip = tdf.groupby("country").count()[["domain"]]
    country_ip["country"] = country_ip.index

    tdf = tdf.drop_duplicates(subset = ["domain", "asn"])
    tdf["asn"] = tdf["asn"].astype("str")
    #tdf = tdf.groupby("asn").count()
    tdf = tdf.groupby("info").count()
    tdf = tdf.sort_values("domain")
    print(len(tdf))
    print(len(tdf[tdf["domain"] == 1]))
    tdf = tdf[tdf["domain"] > 1]
    print(tdf.index.values)
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["domain"], color = "k", edgecolor = "w", alpha = 0.7, label = "Website group count")
    for i in range(len(tdf.index.values)):
        x = tdf["domain"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.5, 8.5])
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
    y_l = ["Liberty Global", "KPN", "Comcast", "RoutIT", "Prolocation", "Time Warner", "Signet", "Zoranet", "ZeroSpace"]
    y_l.reverse()
    ax.set_yticklabels(y_l)
    ax.set_ylabel("AS names", fontproperties = font2)
    ax.set_xlim([0, 4.5])
    ax.set_xticks([i * 0.005 * 211 for i in range(5)])
    ax.set_xticklabels(["0%", "0.5%", "1%", "1.5%", "2%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)

    tdf = df[df["cond_type"] == "location"]
    tdf["country"] = tdf["cond_value"].apply(lambda s: s.split("|")[0])
    tdf = tdf.drop_duplicates(subset = ["domain", "country"])
    tdf = tdf.groupby("country").count()[["domain"]]
    tdf["country"] = tdf.index
    tdf = tdf.merge(country_ip, on = "country")
    print(len(tdf["domain_x"]))
    print(pearsonr(tdf["domain_x"], tdf["domain_y"]))
