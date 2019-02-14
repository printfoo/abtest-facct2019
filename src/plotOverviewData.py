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
    domain_rank_path = os.path.join(file_path, "data", "optimizely_domain_rank.csv")
    fig_path = os.path.join(file_path, "results", "overview_distribution.pdf")
    fig2_path = os.path.join(file_path, "results", "overview_domain_rank.pdf")
    
    # read and plot
    df = pd.read_csv(overview_path, sep = "\t")
    df = df.groupby("domain").sum()
    df = df[df["use_optimizely"] > 0]
    print(df)
    df["percentage"] = df["use_optimizely"] / df["crawl_count"]
    print(len(df))
    print(len(df[df["percentage"] == 1]))
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    bins1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.999]
    bins2 = [0.999, 1.099]
    hist2 = ax.hist(df["percentage"], bins = bins2, color = "k", edgecolor = "w", alpha = 0.7, label = "Using \u201cfull-on\u201d mode")
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
    ax.set_xlabel("Percentage of web pages", fontproperties = font2)
    ax.set_ylim([0, 340])
    ax.set_yticks([i * 0.1 * 575 for i in range(6)])
    ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%", "50%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    #ax.legend(loc = 2, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)

    # read and plot
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    df = pd.read_csv(domain_rank_path)
    """
    ys = [i + 1 for i in range(1000000)]
    x1 = []
    x2 = []
    for y in ys:
        tdf = df[df["rank"] == y]
        if not tdf.empty:
            x1.append(1)
            if tdf.iloc[0]["use_optimizely"] > 0:
                x2.append(1)
            else:
                x2.append(0)
        else:
            x1.append(0)
            x2.append(0)
    print(pearsonr(ys, x1))
    print(pearsonr(ys, x2))
    """
    heights, bins = np.histogram(df["rank"], bins = 20, normed = True)
    bins_mid = bins[:-1] + np.diff(bins) / 2
    #ax.plot(bins_mid, heights, color = "k", linestyle = ":", label = "Contacted Optimizely")
    heights, bins = np.histogram(df[df["use_optimizely"] > 0]["rank"], bins = 20, normed = True)
    bins_mid = bins[:-1] + np.diff(bins) / 2
    ax.plot(bins_mid, heights, color = "k", linestyle = "-",  label = "Used Optimizely")
    ax.set_ylim([-0.0000002, 0.0000102])
    ax.set_yticks([0.000002 * i for i in range(6)])
    ax.set_yticklabels([0, r"$0.2\times10^{-5}$", r"$0.4\times10^{-5}$", r"$0.6\times10^{-5}$", r"$0.8\times10^{-5}$", r"$1.0\times10^{-5}$"])
    ax.set_ylabel("Probability density", fontproperties = font2)
    ax.set_xlim([0, 1000000])
    ax.set_xticks([200000 * i for i in range(6)])
    ax.set_xticklabels([0, "200k", "400k", "600k", "800k", "1m"])
    ax.set_xlabel("Alexa rank", fontproperties = font2)
    #ax.legend(loc = 1, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)
