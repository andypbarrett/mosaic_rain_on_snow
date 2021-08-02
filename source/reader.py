"""Loaders for data for MOSAiC rain on snow event plots"""

from pathlib import Path

import xarray as xr
import pandas as pd


DATAPATH = Path("/home/apbarret/Data/MOSAiC/met")
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
metfile_path = [DATAPATH / f for f in metfiles]

SNOWDATA_PATH = "/home/apbarret/src/mosaic_rain_on_snow/data/Snow_RoS.csv"
KUKA_PATH = "/home/apbarret/src/mosaic_rain_on_snow/data/KuKa_RoS.csv"
SBR_PATH = Path("/home/apbarret/src/mosaic_rain_on_snow/data")

def metdata():
    """Loads meteorological tower data"""
    ds = xr.open_mfdataset(metfile_path, combine="by_coords")
    return ds


def snowdata():
    """Returns pandas dataframe containing snowpit observations"""
    return pd.read_csv(SNOWDATA_PATH, parse_dates=True, index_col="Timestamp")


def these_columns(x):
    return "Unnamed" not in x

def kukadata():
    """Returns pandas dataframe containing KuKa radar data"""
    df = pd.read_csv(KUKA_PATH, index_col="Date/Time", usecols=these_columns)
    df.index = pd.to_datetime(df.index, format="%m/%d/%Y %H:%M")
    return df


def onesbr(frequency):
    """Reads one of the SBR files"""
    df = pd.read_csv(SBR_PATH / f"tb{frequency}_leg5_calibrated.txt",
                     index_col="Date",
                     parse_dates={"Date": [0, 1]},
                     delim_whitespace=True,
                     header=None,
                     usecols=[0, 1, 21, 22])
    df.columns = [f"{frequency}H", f"{frequency}V"]
    return df


def sbrdata():
    """Load SBR files and join into one DataFrame"""
    df19 = onesbr("19")
    df89 = onesbr("89")
    return df19.join(df89)
