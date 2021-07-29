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

DEFAULT_MARKER_SIZE = 50
DEFAULT_MARKER_COLOR = "c"
DEFAULT_DATA_LINE_COLOR = "black"
DEFAULT_ZERO_LINE_COLOR = "0.3"


def site_legend_handles(color=DEFAULT_MARKER_COLOR, markersize=8):
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


def mscatter(df, column, ax=None, color='k', size=1, label=None):
    """Creates a scatter plot using different markers for each point"""
    if not ax: ax = plt.gca()
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

    if not ax: ax = plt.gca()
    ax.set_xlim(xbeg, xend)
    ax.xaxis.set_major_formatter(datefmt)

    ax.axvspan(ros_beg, ros_end, color='0.8', zorder=0)

    return ax


def plot_meteorological_data(metdata, ax=None):
    """Creates panel with meteorological data
    :metdata: xarray.DataFrame containing meteorological tower data

    :ax: matplotlib.Axes instance
    """
    tair_min_limit = -20.
    tair_max_limit = 3.
    ax = plot_panel(ax)
    metdata.temp_2m.plot(ax=ax, color=DEFAULT_DATA_LINE_COLOR, lw=2)
    ax.axhline(0., c=DEFAULT_ZERO_LINE_COLOR)
    ax.set_ylim(tair_min_limit, tair_max_limit)
    ax.set_xlabel('')
    ax.set_ylabel('Tair $^{\circ}C$')
    return ax


def plot_snow_temperature(metdata, snowdata, ax=None):
    """Creates panel with snow temperature data
    :metdata: xarray.DataSet with meteorological data
    :snowdata: pandas.DataFrame with snow data

    :ax: matplotlib.Axes instance
    """
    ax = plot_panel(ax)
    ax.axhline(0., c=DEFAULT_ZERO_LINE_COLOR)
    ax.set_ylim(-20, 3)
    metdata.brightness_temp_surface.plot(
        ax=ax,
        color=DEFAULT_DATA_LINE_COLOR,
        label='Snow surface temperature'
    )
    ax = mscatter(snowdata,
                  'Bulk Temp (C)',
                  ax=ax,
                  color=DEFAULT_MARKER_COLOR,
                  size=DEFAULT_MARKER_SIZE
                  )
    ax.set_xlabel('')
    ax.set_ylabel('Tsnow ($^{\circ}C$)')

    # Make snow temperature legend
    handles, labels = ax.get_legend_handles_labels()
    marker_handle = mlines.Line2D([], [],
                                  color=DEFAULT_MARKER_COLOR,
                                  marker="o",
                                  linestyle='None',
                                  markersize=8)
    handles.append(marker_handle)
    labels.append("Bulk snow temperature")
    ax.legend(handles, labels, loc="lower right")
    return ax


def plot_snow_density(snowdata, ax=None):
    """Create plot of snow density parameters.  Plots bulk density,
       desnity from micro-CT and SSA from micro-CT
    :snowdata: pandas.DataFrame containing snow data
    
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plot_panel(ax)
    ax = mscatter(snowdata, 'Bulk snow density',
                  ax=ax, color=density_colors[0],
                  size=DEFAULT_MARKER_SIZE)
    ax = mscatter(snowdata, 'density',
                  ax=ax, color=density_colors[1],
                  size=DEFAULT_MARKER_SIZE)
    ax.set_ylim(120., 370)
    ax.set_ylabel('Density ($kg m^{-3}$)')

    # Add sencond y-axis for SSA
    ax_ssa = ax.twinx()
    ax_ssa = mscatter(snowdata, 'SSA',
                      ax=ax_ssa,
                      color=density_colors[2],
                      size=DEFAULT_MARKER_SIZE)
    ax_ssa.set_ylim(0., 25.)
    ax_ssa.set_ylabel('Specific Surface Area ($m^2 kg^{-1}$)')

    ax.legend(handles=density_legend_handles())
    return ax


def plot_snow_water_equivalent(snowdata, ax=None):
    """Creates plots of snow water equivalent
    :snowdata: pandas.DataFrame containing snow data
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plot_panel(ax)
    ax = mscatter(snowdata, 'SWE (mm)',
                  ax=ax,
                  color=DEFAULT_MARKER_COLOR,
                  size=DEFAULT_MARKER_SIZE)
    ax.set_ylim(0., 35)
    ax.set_ylabel('SWE (mm)')
    return ax


def plot_snow_salinity(snowdata, ax=None):
    """Create plot of snow salinity observations.
    :snowdata: pandas.DataFrame containing snow data
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plot_panel(ax)
    ax = mscatter(snowdata, 'Salinity [ppt]',
                  ax=ax,
                  color=DEFAULT_MARKER_COLOR,
                  size=DEFAULT_MARKER_SIZE)
    ax.set_ylim(-0.05, 0.6)
    ax.set_ylabel('Salinity (ppt)')
    ax.legend(handles=site_legend_handles(), loc="upper left")
    return ax


def plot_snowdata_and_met():
    """Plots air temperature and snowpack parameters for MOSAiC ROS event"""
    metdata = reader.metdata()
    snowdata = reader.snowdata()

    fig, ax = plt.subplots(5, 1, figsize=(7,9), sharex=True)

    ax[0] = plot_meteorological_data(metdata, ax=ax[0])
    ax[1] = plot_snow_temperature(metdata, snowdata, ax=ax[1])
    ax[2] = plot_snow_density(snowdata, ax=ax[2])
    ax[3] = plot_snow_water_equivalent(snowdata, ax=ax[3])
    ax[4] = plot_snow_salinity(snowdata, ax=ax[4])

    plt.tight_layout(h_pad=0.01)
    plt.show()


if __name__ == "__main__":
    plot_snowdata_and_met()
