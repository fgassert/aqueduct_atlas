"""
"""

import numpy as np
import sys
import matplotlib.mlab as mlab
import flowaccumulator as fa
import gen_merge
import arcpy as ap
from constants import *

args = (BASINCSV, BASINPOLY, STORAGE_PTS, STORAGECSV)

TMP_OUT = "in_memory/tmp"

def f0(i, x):
    return np.max(x[i],0)

def f(i, idx, values, x):
    return np.sum(values[idx]) + f0(i, x)

def main(basin_csv, basin_poly, storage_pts, stor_csv):
    basin_rec = mlab.csv2rec(basin_csv)

    ids = basin_rec["basinid"]
    d_ids = basin_rec["dwnbasinid"]

    ap.Identity_analysis(storage_pts, basin_poly, TMP_OUT, "NO_FID")
    out = ap.da.FeatureClassToNumPyArray(TMP_OUT,[STOR_FIELD,BASIN_ID_FIELD])

    stor = np.array([np.sum(out[STOR_FIELD][out[BASIN_ID_FIELD]==i]) for i in ids])

    fa_stor = fa.accumulate(ids,d_ids,f0,f,stor)

    outrec = np.rec.fromarrays((ids,stor,fa_stor),names=("basinid","stor","fa_stor"))
    
    mlab.rec2csv(outrec, stor_csv)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1:])
    else:
        main(*args)
