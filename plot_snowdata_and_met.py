"""Plots air temperature and snowpack parameters for MOSAiC ROS event"""
import datetime as dt

import matplotlib.pyplot as plt

import reader


def plot_panel(ax):
    """Adds a plot panel"""
    xbeg = dt.datetime(2020, 9, 9, 0)
    xend = dt.datetime(2020, 9, 16, 0)
    ax.set_xlim(xbeg, xend)
    return ax

def plot_snowdata_and_met():
    """Plots air temperature and snowpack parameters for MOSAiC ROS event"""
    metdata = reader.metdata()
    snowdata = reader.snowdata()

    fig, ax = plt.subplots(5, 1, figsize=(7,9))
    plot_panel(ax[0])
    
    return


if __name__ == "__main__":
    plot_snowdata_and_met()
    
