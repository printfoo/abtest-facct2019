#!/usr/local/bin/python3

import os, sys, json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from scipy.stats import ttest_ind, bartlett, normaltest, ttest_1samp
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
    bias_path = os.path.join(file_path, "data", "twitter_share_score.csv")
    eco_path = os.path.join(file_path, "data", "misinfo_eco.csv")
    fig_path = os.path.join(file_path, "results", "risk_optimizely_bias.pdf")
    fig2_path = os.path.join(file_path, "results", "risk_overall_bias.pdf")
    
    # plot bias
    bias = pd.read_csv(bias_path)
    bias = bias[bias["twitter_share_base"] > 10]
    l1 = bias["twitter_share_bias"]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    bins1 = [-1, -0.75]
    hist1 = ax.hist(bias["twitter_share_bias"], bins = bins1, color = "cornflowerblue", edgecolor = "w", alpha = 1)
    ax.text(sum(bins1)/2, hist1[0][0], str(int(hist1[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins2 = [-0.75, -0.5]
    hist2 = ax.hist(bias["twitter_share_bias"], bins = bins2, color = "cornflowerblue", edgecolor = "w", alpha = 0.8)
    ax.text(sum(bins2)/2, hist2[0][0], str(int(hist2[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins3 = [-0.5, -0.25]
    hist3 = ax.hist(bias["twitter_share_bias"], bins = bins3, color = "cornflowerblue", edgecolor = "w", alpha = 0.6)
    ax.text(sum(bins3)/2, hist3[0][0], str(int(hist3[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins4 = [-0.25, 0]
    hist4 = ax.hist(bias["twitter_share_bias"], bins = bins4, color = "cornflowerblue", edgecolor = "w", alpha = 0.4)
    ax.text(sum(bins4)/2, hist4[0][0], str(int(hist4[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins5 = [0, 0.25]
    hist5 = ax.hist(bias["twitter_share_bias"], bins = bins5, color = "indianred", edgecolor = "w", alpha = 0.4)
    ax.text(sum(bins5)/2, hist5[0][0], str(int(hist5[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins6 = [0.25, 0.5]
    hist6 = ax.hist(bias["twitter_share_bias"], bins = bins6, color = "indianred", edgecolor = "w", alpha = 0.6)
    ax.text(sum(bins6)/2, hist6[0][0], str(int(hist6[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins7 = [0.5, 0.75]
    hist7 = ax.hist(bias["twitter_share_bias"], bins = bins7, color = "indianred", edgecolor = "w", alpha = 0.8)
    ax.text(sum(bins7)/2, hist7[0][0], str(int(hist7[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins8 = [0.75, 1]
    hist8 = ax.hist(bias["twitter_share_bias"], bins = bins8, color = "indianred", edgecolor = "w", alpha = 1)
    ax.text(sum(bins8)/2, hist8[0][0], str(int(hist8[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    ax.set_ylim([0, 16000])
    ax.set_yticks([i * 0.05 * len(bias) for i in range(5)])
    ax.set_yticklabels(["0%", "5%", "10%", "15%", "20%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    ax.set_xlim([-1, 1])
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xlabel("Partisan bias score", fontproperties = font2)
    ax.axvline(bias["twitter_share_bias"].mean(), color = "k", linestyle = ":")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)

    # read and plot
    df = pd.read_csv(overview_path, sep = "\t")
    df = df.groupby("domain").sum()
    df = df[df["use_optimizely"] > 0]
    df["domain"] = df.index
    bias = df.merge(bias, on = "domain")
    l2 = bias["twitter_share_bias"]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(3, 2))
    bins1 = [-1, -0.75]
    hist1 = ax.hist(bias["twitter_share_bias"], bins = bins1, color = "cornflowerblue", edgecolor = "w", alpha = 1)
    ax.text(sum(bins1)/2, hist1[0][0], str(int(hist1[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins2 = [-0.75, -0.5]
    hist2 = ax.hist(bias["twitter_share_bias"], bins = bins2, color = "cornflowerblue", edgecolor = "w", alpha = 0.8)
    ax.text(sum(bins2)/2, hist2[0][0], str(int(hist2[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins3 = [-0.5, -0.25]
    hist3 = ax.hist(bias["twitter_share_bias"], bins = bins3, color = "cornflowerblue", edgecolor = "w", alpha = 0.6)
    ax.text(sum(bins3)/2, hist3[0][0], str(int(hist3[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins4 = [-0.25, 0]
    hist4 = ax.hist(bias["twitter_share_bias"], bins = bins4, color = "cornflowerblue", edgecolor = "w", alpha = 0.4)
    ax.text(sum(bins4)/2, hist4[0][0], str(int(hist4[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins5 = [0, 0.25]
    hist5 = ax.hist(bias["twitter_share_bias"], bins = bins5, color = "indianred", edgecolor = "w", alpha = 0.4)
    ax.text(sum(bins5)/2, hist5[0][0], str(int(hist5[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins6 = [0.25, 0.5]
    hist6 = ax.hist(bias["twitter_share_bias"], bins = bins6, color = "indianred", edgecolor = "w", alpha = 0.6)
    ax.text(sum(bins6)/2, hist6[0][0], str(int(hist6[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins7 = [0.5, 0.75]
    hist7 = ax.hist(bias["twitter_share_bias"], bins = bins7, color = "indianred", edgecolor = "w", alpha = 0.8)
    ax.text(sum(bins7)/2, hist7[0][0], str(int(hist7[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    bins8 = [0.75, 1]
    hist8 = ax.hist(bias["twitter_share_bias"], bins = bins8, color = "indianred", edgecolor = "w", alpha = 1)
    ax.text(sum(bins8)/2, hist8[0][0], str(int(hist8[0][0])), ha = "center", va = "bottom", color = "k", fontproperties = font3)
    ax.set_ylim([0, 60])
    ax.set_yticks([i * 0.05 * len(bias) for i in range(7)])
    ax.set_yticklabels(["0%", "5%", "10%", "15%", "20%", "25%", "30%"])
    ax.set_ylabel("Percentage of websites", fontproperties = font2)
    ax.set_xlim([-1, 1])
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xlabel("Partisan bias score", fontproperties = font2)
    ax.axvline(bias["twitter_share_bias"].mean(), color = "k", linestyle = ":")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
    
    print(len(l1))
    print(len(l2), len(df), len(l2)/len(df))
    print(l1.mean(), l2.mean())
    print(normaltest(l2))
    print(ttest_1samp(l2, 0))
    print(l1.std(), l2.std())
    print(ttest_ind(l2, l1))
    print(bartlett(l2, l1))

    for a in [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75]:
        b = a + 0.25
        tbias = bias[bias["twitter_share_bias"] >= a]
        tbias = tbias[tbias["twitter_share_bias"] < b].sort_values("twitter_share_base", ascending = False)
        print(a, b)
        print(tbias["domain"].values)
