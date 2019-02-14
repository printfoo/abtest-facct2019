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
    alexa_path = os.path.join(file_path, "data", "alexa_top1m.csv")
    fig_path = os.path.join(file_path, "results", "audience_number_distribution.pdf")
    fig2_path = os.path.join(file_path, "results", "audience_type_distribution.pdf")
    fig3_path = os.path.join(file_path, "results", "audience_device_distribution.pdf")
    fig4_path = os.path.join(file_path, "results", "audience_browser_distribution.pdf")
    
    # read and plot
    df = pd.read_csv(audience_path, sep = "\t")
    #print(df["audience_id"].drop_duplicates())
    for domain in ["optimizely.com", "nytimes.com", "airasia.com", "credomobile.com", "teespring.com"]:
        print(len(df[df["domain"] == domain]["audience_id"].drop_duplicates()))
    
    #print(df[df["cond_value"] == "ucbrowser"])
    print(df[df["domain"] == "teespring.com"])
    
    # number distribution
    tdf = df.drop_duplicates(subset = ["domain", "audience_id"])
    tdf = tdf.groupby("domain").count().sort_values("crawl_time")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    tdf["crawl_time"] = tdf["crawl_time"].apply(lambda x: x if x < 55 else 55)
    bins1 = [1, 6]
    bins2 = [6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56]
    hist1 = ax.hist(tdf["crawl_time"], bins = bins1, color = "k", edgecolor = "w", alpha = 0.7, label = "Using \u201clite\u201d functionality")
    hist2 = ax.hist(tdf["crawl_time"], bins = bins2, color = "k", edgecolor = "w", alpha = 0.7, label = "Other websites")
    bins = bins1 + bins2[1:]
    print(hist1, hist2)
    histx = list(hist1[1]) + list(hist2[1])[1:]
    histy = list(hist1[0]) + list(hist2[0])[0:]
    for i in range(len(bins[:-1])):
        x = histx[i]/2 + histx[i+1]/2
        y = histy[i]
        ax.text(x, y, str(int(y)), ha = "center", va = "bottom", color = "k", fontproperties = font3)

    ax.set_xlim([1, 55])
    ax.set_xticks([1, 10, 20, 30, 40, 50])
    ax.set_xticklabels([1, 10, 20, 30, 40, "50+"])
    ax.set_xlabel("Audience count", fontproperties = font2)
    ax.set_ylim([0, 185])
    ax.set_yticks([i * 0.2 * 211 for i in range(5)])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 1, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
    
    # type distribution
    sel_types = {"browser_version", "cookies", "device", "ip", "location", "platform", "language"}
    df["type"] = df["cond_type"].apply(lambda x: x if x in sel_types else "customized")
    df["type"] = df["type"].apply(lambda x: get_label(x))
    for type in sel_types:
        tmp = df.drop_duplicates(subset = {"audience_id"})
        tmp = tmp[tmp["type"] == get_label(type)].groupby("domain").count().sort_values("crawl_time")[["crawl_time"]]
        print(type, tmp)
    tdf = df.drop_duplicates(subset = ["domain", "type"])
    tdf = tdf.groupby("type").count()
    tdf = tdf.sort_values("domain")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["domain"], color = "k", edgecolor = "w", alpha = 0.7, label = "Website group count")
    for i in range(len(tdf.index.values)):
        x = tdf["domain"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.42, 7.42])
    ax.set_ylabel("Type of audiences", fontproperties = font2)
    ax.set_xlim([0, 145])
    ax.set_xticks([i * 0.1 * 211 for i in range(7)])
    ax.set_xticklabels(["0%", "10%", "20%", "30%", "40%", "50%", "60%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)

    # device distribution
    tdf = df[df["type"] == "Device"]
    tdf["cond_value"] = tdf["cond_value"].apply(lambda x: get_device(x))
    tdf = tdf.drop_duplicates(subset = ["domain", "cond_value"])
    tdf = tdf.groupby("cond_value").count()
    tdf = tdf.sort_values("domain")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["domain"], color = "k", edgecolor = "w", alpha = 0.7, label = "Website group count")
    for i in range(len(tdf.index.values)):
        x = tdf["domain"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.42, 4.42])
    ax.set_ylabel("Device", fontproperties = font2)
    ax.set_xlim([0, 105])
    ax.set_xticks([i * 0.1 * 211 for i in range(6)])
    ax.set_xticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig3_path, bbox_inches = "tight", pad_inches = 0)

    # browser distribution
    tdf = df[df["type"] == "Browser"]
    tdf["cond_value"] = tdf["cond_value"].apply(lambda x: get_browser(x))
    tdf = tdf.drop_duplicates(subset = ["domain", "cond_value"])
    tdf = tdf.groupby("cond_value").count()
    tdf = tdf.sort_values("domain")
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.barh(tdf.index, tdf["domain"], color = "k", edgecolor = "w", alpha = 0.7, label = "Website group count")
    for i in range(len(tdf.index.values)):
        x = tdf["domain"].values[i]
        y = i
        ax.text(x, y, str(x), ha = "left", va = "center", color = "k", fontproperties = font3)
    ax.set_ylim([-0.42, 6.42])
    ax.set_ylabel("Browser", fontproperties = font2)
    ax.set_xlim([0, 35])
    ax.set_xticks([i * 0.05 * 211 for i in range(4)])
    ax.set_xticklabels(["0%", "5%", "10%", "15%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig4_path, bbox_inches = "tight", pad_inches = 0)
