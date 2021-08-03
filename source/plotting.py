"""Common plotting routines"""
import datetime as dt
import matplotlib.dates as mdates


TAIR_ABOVE_ZERO = (dt.datetime(2020, 9, 13, 10, 0),
                   dt.datetime(2020, 9, 14, 9, 40))

RAIN_EVENT_01 = [dt.datetime(2020, 9, 13, 5, 0),
                 dt.datetime(2020, 9, 13, 10, 0)]
RAIN_EVENT_02 = [dt.datetime(2020, 9, 14, 1, 0),
                 dt.datetime(2020, 9, 14, 4, 0)]

XBEGIN = dt.datetime(2020, 9, 9, 0)  # x-axis minimum
XEND = dt.datetime(2020, 9, 16, 0)   # x-axis maximum


def add_fig_label(label, ax):
    ax.text(0.01, 0.98, label,
            transform=ax.transAxes,
            verticalalignment="top",
            horizontalalignment="left",
            fontsize=15,
            bbox={"facecolor": "white", "edgecolor": "None", "alpha": 0.5})


def add_panel(ax, fig_label):
    """Adds a plot panel"""
    datefmt = mdates.DateFormatter("%d")

    if not ax: ax = plt.gca()
    ax.set_xlim(XBEGIN, XEND)
    ax.xaxis.set_major_formatter(datefmt)

    ax.axvspan(TAIR_ABOVE_ZERO[0], TAIR_ABOVE_ZERO[1],
               color='0.8',
               zorder=0)
    ax.axvspan(RAIN_EVENT_01[0], RAIN_EVENT_01[1],
               hatch='..', fill=False, linestyle='None', zorder=1)
    ax.axvspan(RAIN_EVENT_02[0], RAIN_EVENT_02[1],
               hatch='..', fill=False, linestyle='None', zorder=1)

    if fig_label: add_fig_label(fig_label, ax)

    return ax
