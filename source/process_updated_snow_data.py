"""
Creates new snow data file - minus microCT density from
MOSAiC_ROSevent_12to15092020_PitsOnly_Density_Salinity_updated.csv
MOSAiC_ROSevent_12to15092020_PitsOnly_SnowDepth_SWE_withSMPthickness.csv
"""

from pathlib import Path

import pandas as pd

ROOT_PATH = Path("/home", "apbarret", "src", "mosaic_rain_on_snow", "data")
SALINITY_FILE = ROOT_PATH / "MOSAiC_ROSevent_12to15092020_PitsOnly_Density_Salinity_updated.csv"
SNOWDEPTH_FILE = ROOT_PATH / "MOSAiC_ROSevent_12to15092020_PitsOnly_SnowDepth_SWE_withSMPthickness.csv"


def main():
    """Processes the files"""
    salinity = pd.read_csv(SALINITY_FILE, header=0)
    snowdepth = pd.read_csv(SNOWDEPTH_FILE, header=0,
                            index_col="Device_Operation_ID")

    # Create averge salinity and density from layers
    salinity["thickness"] = salinity["From snow height"] - \
        salinity["To snow height"]
    salinity_grp = salinity.groupby(salinity["Device_Operation_ID"])
    salinity_avg = salinity_grp.agg({"Location": "first",
                                     "Salinity [ppt]": "mean",
                                     "Snow density (cutter)": "mean",
                                     "thickness": "sum"})

    snow_merged = salinity_avg.join(snowdepth.loc[:, ["Timestamp",
                                                      "snow height [cm at SWE measurement]",
                                                      "average thickness along 4.5 m (from SMP)",
                                                      "SWE [mm]"]])
    snow_merged = snow_merged.reset_index()
    snow_merged = snow_merged.set_index("Timestamp", drop=True)

    snow_merged.to_csv(ROOT_PATH / "mosaic_ros_snow_updated.csv")
    return


if __name__ == "__main__":
    main()
    
