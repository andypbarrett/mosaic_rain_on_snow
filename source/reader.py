"""Loaders for data for MOSAiC rain on snow event plots"""

from pathlib import Path

import xarray as xr
import pandas as pd

from plotting import XBEGIN as data_start_time
from plotting import XEND as data_end_time


ROOT_PATH = Path("/home", "apbarret")
MET_DATAPATH = ROOT_PATH / "Data" / "MOSAiC" / "met"
metfiles = [
    'mosflxtowermet.level2.10min.20200909.000000.nc',
    'mosflxtowermet.level2.10min.20200910.000000.nc',
    'mosflxtowermet.level2.10min.20200911.000000.nc',
    'mosflxtowermet.level2.10min.20200912.000000.nc',
    'mosflxtowermet.level2.10min.20200913.000000.nc',
    'mosflxtowermet.level2.10min.20200914.000000.nc',
    'mosflxtowermet.level2.10min.20200915.000000.nc',
    'mosflxtowermet.level2.10min.20200916.000000.nc',
    'mosflxtowermet.level2.10min.20200917.000000.nc',
    'mosflxtowermet.level2.10min.20200918.000000.nc',
]
metfile_path = [MET_DATAPATH / f for f in metfiles]

REPODATA_PATH = ROOT_PATH / "src" / "mosaic_rain_on_snow" / "data"
SNOWSALINITY_PATH = REPODATA_PATH / "mosaic_ros_snow_updated.csv"
SNOWDATA_PATH = REPODATA_PATH / "Snow_RoS.csv"
MICROCT_DATA_PATH = REPODATA_PATH / "MOSAiC_ROSevent_12to15092020_PitsOnly_microCTmeans_updated.csv"
SWEDATA_PATH = REPODATA_PATH / "MOSAiC_ROSevent_12to15092020_PitsOnly_SnowDepth_SWE_new_corrected.csv"
KUKA_PATH = REPODATA_PATH / "KuKa_RoS_corrected_KuKaPy_v2.csv"
SBR_PATH = REPODATA_PATH
PLUVIO_PATH = REPODATA_PATH / "pluvio_ds_2020-09-09 00:00:00_2020-09-20 00:00:00.nc"
KAZR_PATH = REPODATA_PATH / "kazr_ds_2020-09-09 00:00:00_2020-09-20 00:00:00.nc"
PARSIVEL_PATH = REPODATA_PATH / "parsivel_ds_2020-09-09 00:00:00_2020-09-20 00:00:00.nc"


def kazrdata():
    """Loads Ka-band zenith radar vertical velocity"""
    ds = xr.open_dataset(KAZR_PATH)
    ds = ds.sel(time=slice(data_start_time, data_end_time))
    return ds


def precipdata():
    """Load bucket and max diameter data"""
    pluvio = xr.open_dataset(PLUVIO_PATH)
    parsivel = xr.open_dataset(PARSIVEL_PATH)
    df = pd.concat([pluvio.bucket_rt.to_dataframe(),
                    parsivel.diameter_max.to_dataframe()],
                    axis=1)
    df = df[data_start_time:data_end_time]
    return df


def metdata():
    """Loads meteorological tower data"""
    ds = xr.open_mfdataset(metfile_path, combine="by_coords")
    return ds


def snowdata():
    """Returns pandas dataframe containing snowpit observations"""
    snowdata = pd.read_csv(SNOWDATA_PATH, parse_dates=True,
                           index_col="Timestamp")
    microctdata = pd.read_csv(MICROCT_DATA_PATH, parse_dates=True,
                              index_col="Timestamp")
    swedata = pd.read_csv(SWEDATA_PATH, parse_dates=True,
                          index_col="Timestamp")
    snowdata['microCT_snowOnly_density'] = microctdata["microCT_snowOnly_density"]
    snowdata['SWE_SnowOnly_fromMicroCT'] = swedata["SWE_SnowOnly_fromMicroCT []"]
    snowdata["mean_microCT_density"] = microctdata["mean_microCT_density"]
    snowdata["microCT_SnowHeight"] = microctdata["microCT_SnowHeight [mm]"]
    return snowdata


def snow_salinity():
    """Returns snow salinity data"""
    return pd.read_csv(SNOWSALINITY_PATH,
                       parse_dates=True,
                       index_col="Timestamp",
                       usecols=["Timestamp", "Location", "Salinity [ppt]"])


def these_columns(x):
    return "Unnamed" not in x

def kukadata():
    """Returns pandas dataframe containing KuKa radar data"""
    df = pd.read_csv(KUKA_PATH, index_col="Date/Time", usecols=these_columns)
    df.index = pd.to_datetime(df.index, format="%m/%d/%Y %H:%M")
    return df


def onesbr(frequency, resample="1H"):
    """Reads one of the SBR files and returns Tb for angle = 55
    :frequency: frequency of data (19 or 89 GHz)
    :resample: time period for resample
    """
    if frequency == "19":
        usecols = [0, 1, 4, 21, 22]
    else:
        usecols = [0, 1, 4, 22, 23]
    df = pd.read_csv(SBR_PATH / f"tb{frequency}_leg5_calibrated.txt",
                     index_col="Date",
                     parse_dates={"Date": [0, 1]},
                     delim_whitespace=True,
                     header=None,
                     usecols=usecols)
    df.columns = ["angle", f"{frequency}H", f"{frequency}V"]
    df = df[df.angle == 55]
    df = df.drop("angle", axis=1)
    df = df.resample(resample).mean()
    return df


def sbrdata(resample="1H"):
    """Load SBR files and join into one DataFrame"""
    df19 = onesbr("19", resample=resample)
    df89 = onesbr("89", resample=resample)
    return df19.join(df89)
