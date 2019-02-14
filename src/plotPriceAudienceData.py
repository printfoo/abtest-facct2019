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
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    price_path = os.path.join(file_path, "data", "optimizely_price.tsv")
    fig_path = os.path.join(file_path, "results", "price_audience_distribution_websites.pdf")
    fig2_path = os.path.join(file_path, "results", "price_audience_distribution_experiments.pdf")
    
    # read and plot
    df = pd.read_csv(audience_path, sep = "\t")
    price = pd.read_csv(price_path, sep = "\t")
    price = price.dropna().drop_duplicates()
    df = df.merge(price, on = ["domain", "audience_id"])
    print(len(df.groupby("domain").count()))
    print(len(df.groupby("experiment_id").count()))

    # type distribution
    sel_types = {"browser_version", "cookies", "device", "ip", "location", "platform", "language"}
    df["type"] = df["cond_type"].apply(lambda x: x if x in sel_types else "customized")
    df["type"] = df["type"].apply(lambda x: get_label(x))
    tdf = df.drop_duplicates(subset = ["domain", "type"])
    tdf = tdf.groupby("type").count()
    tdf = tdf.sort_values("domain")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["domain"], color = "k", edgecolor = "w", alpha = 0.7, label = "Website group count")
    for i in range(len(tdf.index.values)):
        x = tdf["domain"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.42, 6.42])
    ax.set_ylabel("Type of audiences", fontproperties = font2)
    ax.set_xlim([0, 26])
    ax.set_xticks([i * 0.1 * 40 for i in range(7)])
    ax.set_xticklabels(["0%", "10%", "20%", "30%", "40%", "50%", "60%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)

    sel_types = {"browser_version", "cookies", "device", "ip", "location", "platform", "language"}
    df["type"] = df["cond_type"].apply(lambda x: x if x in sel_types else "customized")
    df["type"] = df["type"].apply(lambda x: get_label(x))
    tdf = df.drop_duplicates(subset = ["experiment_id", "type"])
    tdf = tdf.groupby("type").count()
    tdf = tdf.sort_values("experiment_id")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["experiment_id"], color = "k", edgecolor = "w", alpha = 0.7, label = "Website group count")
    for i in range(len(tdf.index.values)):
        x = tdf["experiment_id"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.42, 6.42])
    ax.set_ylabel("Type of audiences", fontproperties = font2)
    ax.set_xlim([0, 105])
    ax.set_xticks([i * 0.2 * 117 for i in range(5)])
    ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%"])
    ax.set_xlabel("Percentage of experiments", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)
