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

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    experiment_path = os.path.join(file_path, "data", "optimizely_experiment.tsv")
    fig_path = os.path.join(file_path, "results", "experiment_num_distribution.pdf")
    fig2_path = os.path.join(file_path, "results", "experiment_audience_distribution.pdf")
    fig3_path = os.path.join(file_path, "results", "experiment_variation_distribution.pdf")
    
    # read and plot
    df = pd.read_csv(experiment_path, sep = "\t")
    #print(df["experiment_id"].drop_duplicates())
    """
    for domain in ["optimizely.com", "nytimes.com", "airasia.com", "credomobile.com", "teespring.com"]:
        print(len(df[df["domain"] == domain]["experiment_id"].drop_duplicates()))
    print(df[df["domain"] == "teespring.com"].groupby("audience_num").count())
    """
    
    # num distribution
    tdf = df.groupby("domain").count().sort_values("crawl_time")
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
    ax.set_xlabel("Experiment count", fontproperties = font2)
    ax.set_ylim([0, 220])
    ax.set_yticks([i * 0.2 * 297 for i in range(4)])
    ax.set_yticklabels(["0%", "20%", "40%", "60%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 1, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
    
    # audience distribution
    print(df.sort_values("audience_num")[["domain", "experiment_name", "audience_num"]])
    tdf = df[df["audience_num"] >= 6]
    tdf1 = tdf[tdf["domain"] == "airasia.com"]
    tdf2 = tdf[tdf["domain"] == "nytimes.com"]
    print(len(tdf), len(tdf1), len(tdf2))

    df["audience_num"] = df["audience_num"].apply(lambda x: str(x) if x < 8 else "8+")
    tdf = df.groupby("audience_num").count()
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.bar(tdf.index[:2], tdf["domain"][:2], color = "k", edgecolor = "w", alpha = 0.7, label = "Using \u201clite\u201d functionality")
    plt.bar(tdf.index[2:], tdf["domain"][2:], color = "k", edgecolor = "w", alpha = 0.7, label = "Other websites")
    for i in range(len(tdf.index.values)):
        y = tdf["domain"].values[i]
        x = i
        ax.text(x, y, str(y), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    ax.set_xlim([-0.45, 8.45])
    ax.set_xlabel("Audience count", fontproperties = font2)
    ax.set_ylim([0, 1100])
    ax.set_yticks([i * 0.1 * 2358 for i in range(6)])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
    ax.set_ylabel("Percentage of experiments", fontproperties = font2)
    #ax.legend(loc = 1, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)


    # vatiation distribution
    #print(df.sort_values("variation_num")[["domain", "experiment_name", "variation_num"]])
    print(df[df["domain"] == "dmv.org"][["domain", "experiment_name", "variation_num"]])

    df["variation_num"] = df["variation_num"].apply(lambda x: str(x) if x < 8 else "8+")
    tdf = df.groupby("variation_num").count()
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    plt.bar(tdf.index[:2], tdf["domain"][:2], color = "k", edgecolor = "w", alpha = 0.7, label = "Using \u201clite\u201d functionality")
    plt.bar(tdf.index[2:], tdf["domain"][2:], color = "k", edgecolor = "w", alpha = 0.7, label = "Other websites")
    for i in range(len(tdf.index.values)):
        y = tdf["domain"].values[i]
        x = i
        ax.text(x, y, str(y), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    ax.set_xlim([-0.45, 7.45])
    ax.set_xlabel("Variation count", fontproperties = font2)
    ax.set_ylim([0, 1300])
    ax.set_yticks([i * 0.1 * 2358 for i in range(6)])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
    ax.set_ylabel("Percentage of experiments", fontproperties = font2)
    #ax.legend(loc = 1, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig3_path, bbox_inches = "tight", pad_inches = 0)
