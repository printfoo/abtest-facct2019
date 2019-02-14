#!/usr/local/bin/python3

import os, sys, json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
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

# get browser from string
def get_browser(x):
    x = "".join([l for l in x if l.isalpha()])
    browser_map = {"ff": "Firefox", "gc": "Chrome", "ucbrowser": "UC"}
    if x in browser_map.keys():
        return browser_map[x]
    else:
        return x.upper() if len(x) <= 2 else x.capitalize()

# get device from string
def get_device(x):
    browser_map = {"iphone": "iPhone", "ipad": "iPad"}
    if x in browser_map.keys():
        return browser_map[x]
    else:
        return x.capitalize()

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    price_path = os.path.join(file_path, "data", "optimizely_price.tsv")
    fig_path = os.path.join(file_path, "results", "risk_advertisement_distribution.pdf")
    fig2_path = os.path.join(file_path, "results", "risk_advertisement_company.pdf")
    
    # read and plot
    df = pd.read_csv(price_path, sep = "\t")
    print(df)
    exit()
    
    # number distribution
    tdf = df.drop_duplicates(subset = ["domain", "advertisement"])
    tdf = tdf.groupby("domain").count()
    tdf = tdf.sort_values("advertisement")
    print(tdf)
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    tdf["advertisement"] = tdf["advertisement"].apply(lambda x: x if x < 6 else 6)
    tdf["num"] = 1
    tdf = tdf.groupby("advertisement").count()
    #print(tdf.sum())
    #print(tdf)
    hist1 = ax.bar(tdf.index, tdf["num"], color = "k", edgecolor = "w", alpha = 0.7)
    for i in range(len(tdf.index.values)):
        y = tdf["num"].values[i]
        x = i
        ax.text(x + 1, y, str(y), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    ax.set_xlim([0.5, 6.5])
    ax.set_xticks([1, 2, 3, 4, 5, 6])
    ax.set_xticklabels([1, 2, 3, 4, 5, "6+"])
    ax.set_xlabel("Advertisement company count", fontproperties = font2)
    ax.set_ylim([0, 90])
    ax.set_yticks([i * 0.2 * 124 for i in range(4)])
    ax.set_yticklabels(["0%", "20%", "40%", "60%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 1, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
    
    # type distribution
    tdf = df.drop_duplicates(subset = ["domain", "advertisement"])
    tdf = tdf.groupby("advertisement").count().sort_values("domain")
    #print(tdf)
    tdf = tdf[tdf["domain"] >= 4]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["domain"], color = "k", edgecolor = "w", alpha = 0.7)
    for i in range(len(tdf.index.values)):
        x = tdf["domain"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.5, 13.5])
    ax.set_yticks([i for i in range(14)])
    ax.set_yticklabels(["Adition", "Celtra", "Inspectlet", "254A", "FairFax", "Clickable", "TRUSTe", "Adform", "Outbrain", "CrazyEgg", "Demandbase", "Mixpanel", "AmazonAWS", "Clicktale"])
    ax.set_ylabel("Advertisement company", fontproperties = font2)
    ax.set_xlim([0, 17])
    ax.set_xticks([i * 0.02 * 124 for i in range(7)])
    ax.set_xticklabels(["0%", "2%", "4%", "6%", "8%", "10%", "12%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)
