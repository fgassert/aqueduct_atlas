
import pandas as pd
import numpy as np
import pylab as pl

INDATA = 'csvs/bt_diff_rcp85.csv'
AREA = 'csvs/basin_area_20140121'

def main():
    df = pd.read_csv(INDATA)
    df['basin_id'] = np.arange(15006)+1
    df.set_index('basin_id', inplace=True)
    wdf = pd.read_csv(AREA)
    wdf.set_index('basin_id', inplace=True)
    df.join(wdf, inplace=True)
    df.dropna(inplace=True)
    x = np.asarray(df["2040"])
    w = np.asarray(df["F_AREA"])
    sd = np.std(x)
    n, bins, patches = pl.hist(x, 50, normed=1)
    y = pl.normpdf(bins, 0, sd)
    l = pl.plot(bins, y, 'k--', linewidth=1.5)
    pl.show()

if __name__ == "__main__":
    main()
