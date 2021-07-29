"""Plots air temperature and snowpack parameters for MOSAiC ROS event"""
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import reader


def plot_panel(ax):
    """Adds a plot panel"""
    datefmt = mdates.DateFormatter("%d")

    ros_beg = dt.datetime(2020, 9, 13, 12)
    ros_end = dt.datetime(2020, 9, 15, 12)
    
    xbeg = dt.datetime(2020, 9, 9, 0)
    xend = dt.datetime(2020, 9, 16, 0)

    ax.set_xlim(xbeg, xend)
    ax.xaxis.set_major_formatter(datefmt)

    ax.axvspan(ros_beg, ros_end, color='0.5')
    
    return ax


def plot_snowdata_and_met():
    """Plots air temperature and snowpack parameters for MOSAiC ROS event"""
    metdata = reader.metdata()
    snowdata = reader.snowdata()

    fig, ax = plt.subplots(5, 1, figsize=(7,9), sharex=True)
    for axes in ax:
        plot_panel(axes)

    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    plot_snowdata_and_met()
    
