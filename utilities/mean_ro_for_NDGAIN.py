import pandas as pd
import numpy as np

INCSV = "ro_mean_rcp45.csv"
OUTCSV = "ro_mean_rcp45_country.csv"

BASIN_TO_COUNTRY = "basin_to_country.csv"
BASIN_FIELD = "BasinID"
COUNTRY_FIELD = "OBJECTID_1"
OVERLAP = "PERCENTAGE"

def main():
    basindf = pd.read_csv(INCSV)
    basindf[BASIN_FIELD] = np.arange(len(basindf)) + 1
    basindf.set_index(BASIN_FIELD, inplace=True)
    b2c = pd.read_csv(BASIN_TO_COUNTRY)
    calcdf = b2c.merge(basindf, 'left', left_on=BASIN_FIELD, right_index=True)
    print len(calcdf)
    for i in range(1995,2075):
        calcdf[str(i)] = calcdf[str(i)]*calcdf[OVERLAP]/100.0
    sums = calcdf.groupby([COUNTRY_FIELD],sort=True).sum()
    print len(sums)
    sums.to_csv(OUTCSV)

if __name__ == "__main__":
    main()
    
