#!/usr/local/bin/python3

import os, sys, json
import numpy as np
import pandas as pd
import geopandas as gpd
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

# get label from string
def get_label(x):
    x = x.split("_")[0]
    return x.upper() if len(x) <= 2 else x.capitalize()

# get US state from abbr.
def get_us_state(s):
    if s.split("|")[0] == "US" and len(s.split("|")) > 1:
        return s.split("|")[1]
    else:
        return np.nan

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    audience_path = os.path.join(file_path, "data", "optimizely_audience.tsv")
    map_path = os.path.join(file_path, "data", "countries_iso2to3.csv")
    state_path = os.path.join(file_path, "data", "us_states_shapefile")
    contry_tech_path = os.path.join(file_path, "data", "country_tech_index.csv")
    state_tech_path = os.path.join(file_path, "data", "state_tech_index.tsv")
    fig_path = os.path.join(file_path, "results", "audience_location_country_distribution.pdf")
    fig2_path = os.path.join(file_path, "results", "audience_location_us_distribution.pdf")
    fig3_path = os.path.join(file_path, "results", "audience_location_country_tech.pdf")
    fig4_path = os.path.join(file_path, "results", "audience_location_us_tech.pdf")
    
    # read and plot
    df = pd.read_csv(audience_path, sep = "\t")
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    map = pd.read_csv(map_path)
    map["iso_a2"] = map["Alpha-2 code"].apply(lambda s: s.split("\"")[1])
    map["iso_a3"] = map["Alpha-3 code"].apply(lambda s: s.split("\"")[1])
    map = map[["iso_a2", "iso_a3"]].drop_duplicates()
    contry_tech = pd.read_csv(contry_tech_path)
    contry_tech = contry_tech[contry_tech["Indicator"] == "9th pillar Technological readiness"]
    contry_tech = contry_tech[contry_tech["Subindicator Type"] == "Value"]
    contry_tech["iso_a3"] = contry_tech["Country ISO3"]
    contry_tech["tech_index"] = contry_tech["2017-2018"]
    contry_tech = contry_tech[["iso_a3", "tech_index"]]
    gdf = world.merge(map, on = "iso_a3").merge(contry_tech, on = "iso_a3")
    gdf2 = gpd.read_file(state_path)
    state_tech = pd.read_csv(state_tech_path, sep = "\t")
    state_tech["NAME"] = state_tech["State"]
    gdf2 = gdf2.merge(state_tech, on = "NAME")

    # country distribution
    tdf = df[df["cond_type"] == "location"]
    tdf["country"] = tdf["cond_value"].apply(lambda s: s.split("|")[0] if s.split("|")[0] else np.nan)
    tmp = tdf.drop_duplicates(subset = {"audience_id"}).dropna(subset = {"country"})
    tmp = tmp.groupby("domain").count().sort_values("crawl_time")[["crawl_time"]]
    print(tmp)
    tdf = tdf.drop_duplicates(subset = ["domain", "country"])
    tdf = tdf.groupby("country").count()
    tdf["domain"] = tdf["domain"] / 211
    tdf["iso_a2"] = tdf.index
    tdf = gdf.merge(tdf, on = "iso_a2", how = "left")
    tdf["domain"] = tdf["domain"].fillna(0)
    corr = tdf[["domain", "tech_index", "iso_a2"]].dropna(subset = ["domain", "tech_index"]).sort_values("domain")
    print(pearsonr(corr["domain"], corr["tech_index"]))
    #print(tdf.sort_values("domain")[["domain", "name"]])
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(4.5, 2.2))
    tdf.plot(ax = ax, edgecolor = "k", linewidth = 0.5, column = "domain", cmap = "binary", vmax = 0.08)
    #ax.set_axis_off()
    #ax.xaxis.set_major_locator(plt.NullLocator())
    #ax.yaxis.set_major_locator(plt.NullLocator())
    ax.set_xlim([-180, 180])
    ax.set_ylim([-60, 85])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel("Longitude", fontproperties = font2)
    ax.set_ylabel("Latitude", fontproperties = font2)
    fig = ax.get_figure()
    cax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
    sm = plt.cm.ScalarMappable(cmap = "binary", norm = plt.Normalize(vmin = 0, vmax = 0.08))
    sm._A = []
    cbar = fig.colorbar(sm, cax = cax, extend = "max", orientation = "vertical")
    cbar.set_ticks([0, 0.02, 0.04, 0.06, 0.08])
    cbar.set_ticklabels(["0%", "2%", "4%", "6%", "8%"])
    cbar.set_label("Percentage of websites", fontproperties = font2)
    plt.savefig(fig_path, bbox_inches = "tight", pad_inches = 0)
    
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(2.2, 2.2))
    ax.scatter(corr["domain"], corr["tech_index"], color = "k", alpha = 0.6, edgecolor = "none", label = "Country")
    print(corr["domain"].values[-1], corr["tech_index"].values[-1] + 0.08, corr["iso_a2"].values[-1])
    ax.text(corr["domain"].values[-2], corr["tech_index"].values[-2] + 0.08, "UK", ha = "center", va = "bottom", color = "k")
    ax.text(corr["domain"].values[-3], corr["tech_index"].values[-3] + 0.08, corr["iso_a2"].values[-3], ha = "center", va = "bottom", color = "k")
    ax.text(corr["domain"].values[-4], corr["tech_index"].values[-4] + 0.08, corr["iso_a2"].values[-4], ha = "center", va = "bottom", color = "k")
    ax.set_xlim([-0.005, 0.05])
    ax.set_xticks([0, 0.01, 0.02, 0.03, 0.04, 0.05])
    ax.set_xticklabels(["0%", "1%", "2%", "3%", "4%", "5%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    ax.set_ylim([1.6, 6.8])
    ax.set_ylabel("Technology index", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig3_path, bbox_inches = "tight", pad_inches = 0)

    # us distribution
    tdf = df[df["cond_type"] == "location"]
    tdf["us_state"] = tdf["cond_value"].apply(get_us_state)
    tmp = tdf.drop_duplicates(subset = {"audience_id"}).dropna(subset = {"us_state"})
    tmp = tmp.groupby("domain").count().sort_values("crawl_time")[["crawl_time"]]
    print(tmp)
    tdf = tdf.drop_duplicates(subset = ["domain", "us_state"])
    tdf = tdf.groupby("us_state").count()
    tdf["domain"] = tdf["domain"] / 211
    tdf["STUSPS"] = tdf.index
    tdf = gdf2.merge(tdf, on = "STUSPS", how = "left")
    tdf["domain"] = tdf["domain"].fillna(0)
    corr = tdf[["domain", "Average Score", "STUSPS"]].dropna(subset = ["domain", "Average Score"]).sort_values("domain")
    print(pearsonr(corr["domain"], corr["Average Score"]))
    #print(tdf.sort_values("domain")[["domain", "NAME"]])
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(4.5, 2.2))
    tdf.plot(ax = ax, edgecolor = "k", linewidth = 0.5, column = "domain", cmap = "binary", vmax = 0.04)
    #ax.set_axis_off()
    #ax.xaxis.set_major_locator(plt.NullLocator())
    #ax.yaxis.set_major_locator(plt.NullLocator())
    ax.set_xlim([-140, -60])
    ax.set_ylim([24, 50])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel("Longitude", fontproperties = font2)
    ax.set_ylabel("Latitude", fontproperties = font2)
    fig = ax.get_figure()
    cax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
    sm = plt.cm.ScalarMappable(cmap = "binary", norm = plt.Normalize(vmin = 0, vmax = 0.04))
    sm._A = []
    cbar = fig.colorbar(sm, cax = cax, extend = "max", orientation = "vertical")
    cbar.set_ticks([0, 0.01, 0.02, 0.03, 0.04])
    cbar.set_ticklabels(["0%", "1%", "2%", "3%", "4%"])
    cbar.set_label("Percentage of websites", fontproperties = font2)
    plt.savefig(fig2_path, bbox_inches = "tight", pad_inches = 0)

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(2.2, 2.2))
    ax.scatter(corr["domain"], corr["Average Score"], color = "k", alpha = 0.6, edgecolor = "none", label = "Country")
    ax.text(corr["domain"].values[-1], corr["Average Score"].values[-1] + 1, corr["STUSPS"].values[-1], ha = "center", va = "bottom", color = "k")
    ax.text(corr["domain"].values[-2], corr["Average Score"].values[-2] + 1.8, corr["STUSPS"].values[-2], ha = "center", va = "bottom", color = "k")
    ax.text(corr["domain"].values[-3], corr["Average Score"].values[-3] - 5.5, corr["STUSPS"].values[-3], ha = "center", va = "bottom", color = "k")
    ax.set_xlim([-0.005, 0.05])
    ax.set_xticks([0, 0.01, 0.02, 0.03, 0.04, 0.05])
    ax.set_xticklabels(["0%", "1%", "2%", "3%", "4%", "5%"])
    ax.set_xlabel("Percentage of websites", fontproperties = font2)
    ax.set_ylim([22, 86])
    ax.set_ylabel("Technology index", fontproperties = font2)
    #ax.legend(loc = 4, frameon = False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.savefig(fig4_path, bbox_inches = "tight", pad_inches = 0)
