"""Plots air temperature and snowpack parameters for MOSAiC ROS event"""
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

import numpy as np

import reader
import plotting

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


def plot_meteorological_data(metdata, ax=None, fig_label=None):
    """Creates panel with meteorological data
    :metdata: xarray.DataFrame containing meteorological tower data

    :ax: matplotlib.Axes instance
    """
    tair_min_limit = -20.
    tair_max_limit = 3.
    ax = plotting.add_panel(ax, fig_label)
    metdata.temp_2m.plot(ax=ax, color=DEFAULT_DATA_LINE_COLOR, lw=2)
    ax.axhline(0., c=DEFAULT_ZERO_LINE_COLOR)
    ax.set_ylim(tair_min_limit, tair_max_limit)
    ax.set_xlabel('')
    ax.set_ylabel('Tair $^{\circ}C$')
    return ax


def plot_snow_temperature(metdata, snowdata, ax=None, fig_label=None):
    """Creates panel with snow temperature data
    :metdata: xarray.DataSet with meteorological data
    :snowdata: pandas.DataFrame with snow data

    :ax: matplotlib.Axes instance
    """
    ax = plotting.add_panel(ax, fig_label)
    ax.axhline(0., c=DEFAULT_ZERO_LINE_COLOR)
    ax.set_ylim(-20, 3)
    metdata.brightness_temp_surface.plot(
        ax=ax,
        color=DEFAULT_DATA_LINE_COLOR,
        label='Snow surface temperature'
    )
    metdata.temp_2m.plot(
        ax=ax,
        color=DEFAULT_DATA_LINE_COLOR,
        ls=':',
        lw=2,
        label='2 m Air Temperature',
    )
    ax = mscatter(snowdata,
                  'Bulk Temp (C)',
                  ax=ax,
                  color=DEFAULT_MARKER_COLOR,
                  size=DEFAULT_MARKER_SIZE
                  )
    ax.set_xlabel('')
    ax.set_ylabel('Temperature ($^{\circ}C$)')

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


def plot_snow_density(snowdata, ax=None, fig_label=None):
    """Create plot of snow density parameters.  Plots bulk density,
       desnity from micro-CT and SSA from micro-CT
    :snowdata: pandas.DataFrame containing snow data
    
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plotting.add_panel(ax, fig_label)
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

    ax.legend(handles=density_legend_handles(), loc="lower left")
    return ax


def plot_snow_water_equivalent(snowdata, ax=None, fig_label=None):
    """Creates plots of snow water equivalent
    :snowdata: pandas.DataFrame containing snow data
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plotting.add_panel(ax, fig_label)
    ax = mscatter(snowdata, 'SWE (mm)',
                  ax=ax,
                  color=DEFAULT_MARKER_COLOR,
                  size=DEFAULT_MARKER_SIZE)
    ax.set_ylim(0., 35)
    ax.set_ylabel('SWE (mm)')
    return ax


def plot_snow_salinity(snowdata, ax=None, fig_label=None):
    """Create plot of snow salinity observations.
    :snowdata: pandas.DataFrame containing snow data
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plotting.add_panel(ax, fig_label)
    ax = mscatter(snowdata, 'Salinity [ppt]',
                  ax=ax,
                  color=DEFAULT_MARKER_COLOR,
                  size=DEFAULT_MARKER_SIZE)
    ax.set_ylim(-0.05, 0.6)
    ax.set_ylabel('Salinity (ppt)')
    ax.legend(handles=site_legend_handles(), loc="lower left")
    return ax


def plot_snowdata_and_met():
    """Plots air temperature and snowpack parameters for MOSAiC ROS event"""
    metdata = reader.metdata()
    snowdata = reader.snowdata()

    fig, ax = plt.subplots(4, 1, figsize=(7, 9), sharex=True,
                           constrained_layout=True)

    ax[0] = plot_snow_temperature(metdata, snowdata, ax=ax[0], fig_label="a)")
    ax[1] = plot_snow_density(snowdata, ax=ax[1], fig_label="b)")
    ax[2] = plot_snow_water_equivalent(snowdata, ax=ax[2], fig_label="c)")
    ax[3] = plot_snow_salinity(snowdata, ax=ax[3], fig_label="d)")

    fig.set_constrained_layout_pads(h_pad=0.01)
    fig.savefig("mosaic_rain_on_snow_figure01.png")


if __name__ == "__main__":
    plot_snowdata_and_met()
