"""Makes a 3-panel figure showing radar Tb just around ROS event"""
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import seaborn as sns

import reader
from plot_microwave import split_kuka, plot_ka, plot_ku, plot_sbr, kd_plot

XBEGIN = dt.datetime(2020,9,12)
XEND = dt.datetime(2020,9,15)


def plot_mosaic_microwave_closeup():
    """Plots closeup of microwave just around event"""
    kuka = reader.kukadata()
    sbr = reader.sbrdata()

    # 19 GHz values before 2020-09-09 11:00:00 may be affected by
    # moving the antenna, so I set to NaN here
    sbr.loc[:'2020-09-09 11', ['19V', '19H']] = np.nan

    # For now, split Ku and Ka channels into separate Dataframes
    ku_df = split_kuka(kuka, "Ku")
    ka_df = split_kuka(kuka, "Ka")

    datefmt = mdates.DateFormatter('%d\n%H:%M')
    
    fig = plt.figure(figsize=(7, 9), constrained_layout=False)
    gs = GridSpec(3, 6, figure=fig)

    ax0 = fig.add_subplot(gs[0, :-2])
#    ax0 = fig.add_subplot(3, 1, 1)
    plot_ku(ku_df, ax=ax0, fig_label="a) Ku")
    ax0.tick_params(labelbottom=False)
    ax0.set_xlabel('')
    ax0.set_xlim(XBEGIN, XEND)

    ax1 = fig.add_subplot(gs[1, :-2], sharex=ax0)
#    ax1 = fig.add_subplot(3, 1, 2)
    plot_ka(ka_df, ax=ax1, fig_label="b) Ka")
    ax1.tick_params(labelbottom=False)
    ax1.set_xlabel('')
    ax1.set_xlim(XBEGIN, XEND)

    ax2 = fig.add_subplot(gs[2, :-2], sharex=ax0)
#    ax2 = fig.add_subplot(3, 1, 3)
    plot_sbr(sbr, ax=ax2, fig_label="c) SBR")
    ax2.set_xlabel('September 2020')
    ax2.set_xlim(XBEGIN, XEND)
    ax2.xaxis.set_major_formatter(datefmt)

    plt.show()
#    fig.savefig("mosaic_rain_on_snow_microwave.closeup.png")

    return


if __name__ == "__main__":
    plot_mosaic_microwave_closeup()
