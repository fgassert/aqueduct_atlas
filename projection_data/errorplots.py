
import pandas as pd
import numpy as np
import pylab as pl

INDATA = 'csvs/bt_diff_rcp85.csv'

def main():
    df = pd.read_csv(INDATA)
    x = np.asarray(df["2040"].dropna())
    sd = np.std(x)
    n, bins, patches = pl.hist(x, 50, normed=1)
    y = pl.normpdf(bins, 0, sd)
    l = pl.plot(bins, y, 'k--', linewidth=1.5)
    pl.show()

if __name__ == "__main__":
    main()
