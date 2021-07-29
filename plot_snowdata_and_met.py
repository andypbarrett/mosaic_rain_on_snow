"""Plots air temperature and snowpack parameters for MOSAiC ROS event"""
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import reader


site_markers = []

def plot_panel(ax):
    """Adds a plot panel"""
    datefmt = mdates.DateFormatter("%d")

    ros_beg = dt.datetime(2020, 9, 13, 12)
    ros_end = dt.datetime(2020, 9, 15, 12)

    xbeg = dt.datetime(2020, 9, 9, 0)
    xend = dt.datetime(2020, 9, 16, 0)

    ax.set_xlim(xbeg, xend)
    ax.xaxis.set_major_formatter(datefmt)

    ax.axvspan(ros_beg, ros_end, color='0.8')

    return ax


def plot_snowdata_and_met():
    """Plots air temperature and snowpack parameters for MOSAiC ROS event"""
    metdata = reader.metdata()
    snowdata = reader.snowdata()

    fig, ax = plt.subplots(5, 1, figsize=(7,9), sharex=True)

    # Met data
    ax[0] = plot_panel(ax[0])
    metdata.temp_2m.plot(ax=ax[0], color='k', lw=2)
    ax[0].axhline(0., c='0.3')
    ax[0].set_ylim(-20, 3)

    # Snow surface temperature
    ax[1] = plot_panel(ax[1])
    ax[1].axhline(0., c='0.3')
    ax[1].set_ylim(-20, 3)
    metdata.brightness_temp_surface.plot(ax=ax[1], color='k')
    snowdata['Bulk Temp (C)'].plot(ax=ax[1], marker='o', linestyle='')
    
    # Snow density and SSA
    ax[2] = plot_panel(ax[2])

    # Snow salinity
    ax[3] = plot_panel(ax[3])

    # Snow water equivalent
    ax[4] = plot_panel(ax[4])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_snowdata_and_met()
