"""Common plotting routines"""
import datetime as dt
import matplotlib.dates as mdates


def plot_panel(ax, fig_label):
    """Adds a plot panel"""
    datefmt = mdates.DateFormatter("%d")

    ros_beg = dt.datetime(2020, 9, 13, 10, 0)
    ros_end = dt.datetime(2020, 9, 14, 9, 40)

    xbeg = dt.datetime(2020, 9, 9, 0)
    xend = dt.datetime(2020, 9, 16, 0)

    if not ax: ax = plt.gca()
    ax.set_xlim(xbeg, xend)
    ax.xaxis.set_major_formatter(datefmt)

    ax.axvspan(ros_beg, ros_end, color='0.8', zorder=0)

    if fig_label: add_fig_label(fig_label, ax)
    
    return ax


