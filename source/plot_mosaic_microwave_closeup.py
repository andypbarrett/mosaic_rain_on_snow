"""Makes a 3-panel figure showing radar Tb just around ROS event"""
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import seaborn as sns

import reader
from plot_microwave import split_kuka, plot_ka, plot_ku, plot_sbr, kd_plot
from plotting import (PRE_EVENT,
                      POST_EVENT,
                      RADAR_COLORS,
                      RADAR_LINESTYLES,
                      RADAR_SHADE,
                      SBR_COLORS,
                      SBR_LINESTYLES,
                      SBR_SHADE)

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

    # Kernal density plots, following Vishnu's method
    # Ku KDE before event
    ax3 = fig.add_subplot(gs[0, 4], sharey=ax0)
    ax3.tick_params(labelleft=False, left=False,  labelbottom=False)
    kd_plot(ku_df[:PRE_EVENT],
            ku_df.columns,
            RADAR_COLORS,
            RADAR_SHADE,
            RADAR_LINESTYLES,
            ax=ax3,
            fig_label='Pre')
    #print(ax3.get_xlim())

    # Ku KDE after event
    ax6 = fig.add_subplot(gs[0, 5], sharey=ax0)
    ax6.tick_params(labelleft=False, left=False,  labelbottom=False)
    kd_plot(ku_df[POST_EVENT:],
            ku_df.columns,
            RADAR_COLORS,
            RADAR_SHADE,
            RADAR_LINESTYLES,
            ax=ax6,
            fig_label='Post')
    #print(ax6.get_xlim())

    # Ka KDE before event
    ax4 = fig.add_subplot(gs[1, 4], sharey=ax1, sharex=ax3)
    ax4.tick_params(labelleft=False, left=False)
    kd_plot(ka_df[:PRE_EVENT],
            ka_df.columns,
            RADAR_COLORS,
            RADAR_SHADE,
            RADAR_LINESTYLES,
            ax=ax4,
            fig_label=None)
    ax4.set_xlabel('')
    ax4.set_xticks([0., 2.5])
    ax4.set_xticklabels(['0', '2.5'])

    # Ka KDE after event
    ax7 = fig.add_subplot(gs[1, 5], sharey=ax1, sharex=ax6)
    ax7.tick_params(labelleft=False, left=False)
    kd_plot(ka_df[POST_EVENT:],
            ka_df.columns,
            RADAR_COLORS,
            RADAR_SHADE,
            RADAR_LINESTYLES,
            ax=ax7,
            fig_label=None)
    ax7.set_xlabel('')
    ax7.set_xticks([0., 0.25])
    ax7.set_xticklabels(['0', '0.25'])

    # SBR KDE before event
    ax5 = fig.add_subplot(gs[2, 4], sharey=ax2)
    ax5.tick_params(labelleft=False, left=False)
    kd_plot(sbr[:PRE_EVENT],
            sbr.columns,
            SBR_COLORS,
            SBR_SHADE,
            SBR_LINESTYLES,
            ax=ax5,
            fig_label=None)
    ax5.set_xticks([0., 0.25])
    ax5.set_xticklabels(['0', '0.25'])

    # SBR KDE after event
    ax8 = fig.add_subplot(gs[2, 5], sharey=ax2)
    ax8.tick_params(labelleft=False, left=False)
    kd_plot(sbr[POST_EVENT:],
            sbr.columns,
            SBR_COLORS,
            SBR_SHADE,
            SBR_LINESTYLES,
            ax=ax8,
            fig_label=None)
    ax8.set_xticks([0., 0.025])
    ax8.set_xticklabels(['0', '0.025'])

    fig.subplots_adjust(wspace=0.25)

#    plt.show()
    fig.savefig("mosaic_rain_on_snow_microwave.closeup.png")

    return


if __name__ == "__main__":
    plot_mosaic_microwave_closeup()
