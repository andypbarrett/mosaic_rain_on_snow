"""Plots air temperature and snowpack parameters for MOSAiC ROS event"""
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.markers as mmarkers
import matplotlib.lines as mlines

import numpy as np

import reader


site_name = ["ROV",
             "ALBK",
             "CORING",
             "KuKa PIT",
             "FLUX",
             "RS"]
site_markers = ["o", "v", "P", "X", "D", "s"]

density_labels = [
    "Density cutter",
    "micro-CT",
    "SSA"
    ]
density_colors = [
    "c",
    "m",
    "y",
    ]


def site_legend_handles(color='black', markersize=8):
    """Generates legend for site markers"""
    handles = []
    for marker, label in zip(site_markers, site_name):
        handles.append(
            mlines.Line2D([], [],
                          color=color,
                          marker=marker,
                          linestyle='None',
                          markersize=markersize,
                          label=label,)
            )
    return handles


def density_legend_handles(markersize=8):
    """Generates legend for density plot"""
    handles = []
    for label, color in zip(density_labels, density_colors):
        handles.append(
            mlines.Line2D(
                [], [],
                color=color,
                marker='o',
                linestyle='None',
                markersize=markersize,
                label=label,
                )
            )
    return handles


def define_markers():
    """Returns list of marker paths for plotting with mscatter"""
    paths = []
    for m in site_markers:
        mobj = mmarkers.MarkerStyle(m)
        path = mobj.get_path().transformed(mobj.get_transform())
        paths.append(path)
    return paths


def mscatter(df, column, ax=None, color='k', size=1, label=None):
    if not ax: ax=plt.gca()
    xs = df.index.values
    ys = df[column]
    for x, y, m in zip(xs, ys, site_markers):
        if np.isfinite(y):
            ax.scatter(x, y, size, marker=m, c=color, zorder=10, label=label)
    return ax


def plot_panel(ax):
    """Adds a plot panel"""
    datefmt = mdates.DateFormatter("%d")

    ros_beg = dt.datetime(2020, 9, 13, 10, 0)
    ros_end = dt.datetime(2020, 9, 14, 9, 40)

    xbeg = dt.datetime(2020, 9, 9, 0)
    xend = dt.datetime(2020, 9, 16, 0)

    ax.set_xlim(xbeg, xend)
    ax.xaxis.set_major_formatter(datefmt)

    ax.axvspan(ros_beg, ros_end, color='0.8', zorder=0)

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
    ax[0].set_xlabel('')
    ax[0].set_ylabel('Tair $^{\circ}C$')

    # Snow surface temperature
    ax[1] = plot_panel(ax[1])
    ax[1].axhline(0., c='0.3')
    ax[1].set_ylim(-20, 3)
    metdata.brightness_temp_surface.plot(ax=ax[1], color='k',
                                         label='Snow surface temperature')
    ax[1] = mscatter(snowdata, 'Bulk Temp (C)', ax=ax[1], color='blue',
                     size=50)
    ax[1].set_xlabel('')
    ax[1].set_ylabel('Tsnow ($^{\circ}C$)')
    # Make snow temperature legend
    handles, labels = ax[1].get_legend_handles_labels()
    marker_handle = mlines.Line2D([], [], color='blue', marker="o",
                                  linestyle='None', markersize=8)
    handles.append(marker_handle)
    labels.append("Bulk snow temperature")
    ax[1].legend(handles, labels, loc="lower right")

    # Snow density and SSA
    ax[2] = plot_panel(ax[2])
    ax[2] = mscatter(snowdata, 'Bulk snow density', ax=ax[2], color=density_colors[0],
                     size=50)
    ax[2] = mscatter(snowdata, 'density', ax=ax[2], color=density_colors[1],
                     size=50)
    ax_ssa = ax[2].twinx()
    ax_ssa = mscatter(snowdata, 'SSA', ax=ax_ssa, color=density_colors[2], size=50)
    ax_ssa.set_ylim(0., 25.)
    ax_ssa.set_ylabel('Specific Surface Area ($m^2 kg^{-1}$)')
    ax[2].set_ylim(120., 370)
    ax[2].set_ylabel('Density ($kg m^{-3}$)')
    ax[2].legend(handles=density_legend_handles())
    
    # Snow salinity
    ax[3] = plot_panel(ax[3])
    ax[3] = mscatter(snowdata, 'SWE (mm)', ax=ax[3], color='black', size=50)
    ax[3].set_ylim(0., 35)
    ax[3].set_ylabel('SWE (mm)')

    # Snow water equivalent
    ax[4] = plot_panel(ax[4])
    ax[4] = mscatter(snowdata, 'Salinity [ppt]', ax=ax[4], color='black',
                     size=50)
    ax[4].set_ylim(-0.05, 0.6)
    ax[4].set_ylabel('Salinity (ppt)')
    ax[4].legend(handles=site_legend_handles(), loc="upper left")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_snowdata_and_met()
