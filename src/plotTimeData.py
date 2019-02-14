#!/usr/local/bin/python3

import os, sys, json
from scipy.stats import pointbiserialr, pearsonr
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

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    overview_path = os.path.join(file_path, "data", "optimizely_overview.tsv")
    tmp_path = os.path.join(file_path, "data", "tmp.csv")
    fig_path = os.path.join(file_path, "results", "overview_time.pdf")
    
    # read and plot
    df = pd.read_csv(overview_path, sep = "\t")
    df = df.groupby(["domain", "crawl_time"]).sum()
    df["use_optimizely_at_time"] = df["use_optimizely"].apply(lambda x: 1 if x > 0 else 0)
    df[["use_optimizely_at_time"]].to_csv(tmp_path)
    df = pd.read_csv(tmp_path)
    os.remove(tmp_path)
    df = df.groupby("domain").count()
    print(df[df["crawl_time"] > 5])
    exit()
    df["percentage"] = df["use_optimizely"] / df["crawl_count"]
    print(len(df))
    print(len(df[df["percentage"] == 1]))
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    bins1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.999]
    bins2 = [0.999, 1.099]
    hist2 = ax.hist(df["percentage"], bins = bins2, color = "k", edgecolor = "w", alpha = 0.4, label = "Using \u201cfull-on\u201d mode")
    hist1 = ax.hist(df["percentage"], bins = bins1, color = "k", edgecolor = "w", alpha = 0.7, label = "Other websites")
    bins = bins1 + bins2[1:]
    histx = list(hist1[1]) + list(hist2[1])[1:]
    histy = list(hist1[0]) + list(hist2[0])[0:]
    #x = [hist[1][i]/2 + hist[1][i+1]/2 for i in range(len(hist[1][:-1]))]
    #ax.plot(x, hist[0], color = "k")
    print(histy)
    for i in range(len(bins[:-1])):
        x = histx[i]/2 + histx[i+1]/2
        y = histy[i]
        ax.text(x, y, str(int(y)), ha = "center", va = "bottom", color = "k", fontproperties = font3)

    ax.set_xlim([0, 1.1])
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.set_xlabel("Percentage of webpages", fontproperties = font2)
    ax.set_ylim([0, 340])
    ax.set_yticks([i * 0.1 * 575 for i in range(6)])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    ax.legend(loc = 2, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
