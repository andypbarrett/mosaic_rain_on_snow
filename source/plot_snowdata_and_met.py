"""Plots air temperature and snowpack parameters for MOSAiC ROS event"""
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.lines as mlines
import matplotlib.dates as dates

import numpy as np
import pandas as pd

from debug_functions import drop_me as dm



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

DEFAULT_MARKER_SIZE     = 50
DEFAULT_MARKER_COLOR    = "c"
DEFAULT_DATA_LINE_COLOR = "black"
DEFAULT_ZERO_LINE_COLOR = "0.3"

SWE_MARKER_COLOR        = "lightcoral"
SALINITY_MARKER_COLOR   = "cornflowerblue"
TOTAL_PRECIP_LINE_COLOR = "m"
DIAMETER_LINE_COLOR     = "black"


def site_legend_handles(color="grey", markersize=8):
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


def mscatter(df, column, ax=None, color='k', size=1, label=None, background=None):
    """Creates a scatter plot using different markers for each point"""
    if not ax: ax = plt.gca()
    xs = df.index.values
    ys = df[column]
    for x, y, m in zip(xs, ys, site_markers):
        if background != None:
            ax.scatter(x, y, size*2.5, marker=m, c=background, zorder=10, label=label)
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
        color='c',
        lw=2,
        label='Snow surface temperature'
    )
    metdata.temp_2m.plot(
        ax=ax,
        color=DEFAULT_DATA_LINE_COLOR,
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

def calc_precip_rate(bucketdata):

    hourly_range = pd.date_range(bucketdata.index[0], bucketdata.index[-1], freq="60min")
    
    means = []
    times = []
    bd = bucketdata.bucket_rt
    for ihour, hour in enumerate(hourly_range):

        try:
            means.append(bd[hour:hourly_range[ihour+1]].mean())
            times.append(hour)
        except Exception as e:
            do_nothing = True # last index will fail
            
    rates = []
    for imean, mean in enumerate(means):
        try: rates.append(means[imean+1] - mean)
        except: do_nothing = True # should only fail on last calculation (index offset)

    rate_df = pd.DataFrame(rates, index=times[0:-1], columns=['precip_rate'])
    

    df_reindexed = rate_df.reindex(index = bd.index)
    final_df = df_reindexed.interpolate(method = 'linear')
    return final_df

def plot_precip_vars(precipdata, ax=None, fig_label=None):
    """Create  plot of size distribution and precip rate (pluvio+parsivel).  

    :snowdata: pandas.DataFrame containing snow data
    
    :ax: matplotlib.Axes
    """

    precipdata['bucket_rt'] = precipdata['bucket_rt'] - precipdata.bucket_rt[precipdata.bucket_rt.isna()==False][0]
    precipdata['bucket_rt'][precipdata['bucket_rt'] <0] = np.nan
    precipdata = pd.concat([precipdata, calc_precip_rate(precipdata.copy())], axis=1)
    precipdata = precipdata.to_xarray()

    if not ax: ax = plt.gca()
    ax = plotting.add_panel(ax, fig_label)
    precipdata.diameter_max.plot(
        ax=ax,
        color=DIAMETER_LINE_COLOR,
        lw=2,
        label='Max diameter',
    )

    #ax.set_ylim(120., 370)
    ax.set_ylabel('Diameter ($mm$)')

    # Add sencond y-axis for SSA
    ax_ssa = ax.twinx()
    if not ax : ax = plt.gca()
    precipdata.precip_rate.plot(
        ax=ax_ssa,
        color=TOTAL_PRECIP_LINE_COLOR,
        lw=2,
        label='Precip rate',
    )
 
    #ax_ssa.set_ylim(0., 25.)
    ax_ssa.set_ylabel('Rate ($mm/hr$)')

    # Make snow temperature legend
    handles, labels = ax.get_legend_handles_labels()
    handles_ssa, labels_ssa = ax_ssa.get_legend_handles_labels()
    ax.legend(handles+handles_ssa, labels+labels_ssa, loc="upper right")
    return ax


def plot_fall_speed(kazrdata, ax=None, fig_label=None):

    kazrdata['range'] = kazrdata.range/1000.0
    range_lims = (0, 10)


    cb_kwargs = {"shrink" : 0.9,
                 "orientation" : "vertical",
                 "pad" : -0.08,
                 "aspect" : 15,
                 "location" : 'right',
                 "label" : "Fall speed ($m/s$)"}

    if not ax: ax = plt.gca()
    ax = plotting.add_panel(ax, fig_label)

    kazrdata.mean_doppler_velocity.plot(ax=ax, 
                                        x='time', y='range', 
                                        ylim=range_lims, 
                                        cbar_kwargs=cb_kwargs, vmin=-3, vmax=3, 
                                        label='Fall speed',
                                        cmap='PRGn')
 
    ax.set_ylabel(f'Height [km]')

    return ax


def plot_snow_salinity_swe(snowdata, salinitydata, ax=None, fig_label=None):
    """Create plot of snow salinity observations.
    :snowdata: pandas.DataFrame containing snow data
    :ax: matplotlib.Axes
    """
    if not ax: ax = plt.gca()
    ax = plotting.add_panel(ax, fig_label)
    ax = mscatter(snowdata, 'Salinity [ppt]',
                  ax=ax,
                  color="grey",
                  size=DEFAULT_MARKER_SIZE,
                  background=SALINITY_MARKER_COLOR,
                  )

    ax.set_ylim(-0.005, 0.15)
    ax.set_ylabel('Salinity (ppt)')
    ax.axhline(0., c=DEFAULT_ZERO_LINE_COLOR)

    # Add sencond y-axis for SSA
    ax_ssa = ax.twinx()
    mscatter(salinitydata, 'SWE (mm)',
                  ax=ax_ssa,
                  color="grey", 
                  size=DEFAULT_MARKER_SIZE,
                  background=SWE_MARKER_COLOR,
             )
    ax_ssa.set_ylim(0., 35)
    ax_ssa.set_ylabel('SWE (mm)')
    ax.legend(handles=site_legend_handles(), loc="lower left")

    #ax.spines['left'].set_color(SALINITY_MARKER_COLOR)
    ax.tick_params(axis='y', colors=SALINITY_MARKER_COLOR)
    ax_ssa.tick_params(axis='y', colors=SWE_MARKER_COLOR)
    ax_ssa.spines['right'].set_color(SWE_MARKER_COLOR)
    ax_ssa.spines['left'].set_color(SALINITY_MARKER_COLOR)


    return ax


def plot_snowdata_and_met():
    """Plots air temperature, precip, and snowpack parameters for MOSAiC ROS event"""
    metdata       = reader.metdata()
    snowdata      = reader.snowdata()
    snow_salinity = reader.snow_salinity()
    hydmet_data   = reader.precipdata()

    # get precip data, but the pickles don't quite line up
    time_start = (mdf := metdata.lat_tower.to_dataframe()).index[0] # walrus abuse
    time_end   = mdf.index[-144]
    precipdata = pd.concat([hydmet_data['pluvio'].bucket_rt.to_dataframe(), hydmet_data['parsivel'].diameter_max.to_dataframe()], axis=1)
    precipdata = precipdata[time_start:time_end]
    kazrdata   = hydmet_data['kazr'].sel(time=slice(time_start, time_end))

    fig, ax = plt.subplots(5, 1, figsize=(7, 11), sharex=True, constrained_layout=True)

    ax[0] = plot_snow_temperature      (metdata, snowdata,       ax=ax[0], fig_label="a)")
    ax[1] = plot_precip_vars           (precipdata,              ax=ax[1], fig_label="b)")
    ax[2] = plot_fall_speed            (kazrdata,                ax=ax[2], fig_label="c)")
    ax[3] = plot_snow_density          (snowdata,                ax=ax[3], fig_label="d)")
    ax[4] = plot_snow_salinity_swe     (snow_salinity, snowdata, ax=ax[4], fig_label="e)")


    date_form = dates.DateFormatter("%m-%d")
    ax[4].xaxis.set_major_formatter(date_form)


    fig.set_constrained_layout_pads(h_pad=0.01)
    fig.savefig("mosaic_rain_on_snow_figure01.png")
    
    dm(locals(),0)

if __name__ == "__main__":
    plot_snowdata_and_met()
