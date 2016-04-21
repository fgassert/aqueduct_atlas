"""
"""

import numpy as np
import sys
import matplotlib.mlab as mlab
import flowaccumulator as fa
import gen_merge
from constants import *

args = (BASINCSV, WITHDRAWALCSV, CONSUMPTIONCSV, FANCONSCSV)

def f0(i, unc):
    return unc[i]

def f(i, idx, values, unc):
    return np.sum(values[idx]) + f0(i, unc)

def main(basin_csv, ut_csv, uc_csv, ncons_csv):
    basin_rec = mlab.csv2rec(basin_csv)

    uc_rec = mlab.csv2rec(uc_csv)
    ut_rec = mlab.csv2rec(ut_csv)

    ids = basin_rec["basinid"]
    d_ids = basin_rec["dwnbasinid"]
     
    uc = gen_merge.arrange_vector_by_ids(uc_rec["ct"],uc_rec["basinid"],ids)
    ut = gen_merge.arrange_vector_by_ids(ut_rec["ut"],ut_rec["basinid"],ids)
    unc = ut - uc

    n = len(ids)

    ncons = fa.accumulate(ids,d_ids,f0,f,unc)

    outrec = np.rec.fromarrays((ids,ncons),names=("basinid","ncons"))
    
    mlab.rec2csv(outrec, ncons_csv)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1:])
    else:
        main(*args)
