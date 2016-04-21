"""

"""

import numpy as np
import sys
import matplotlib.mlab as mlab
import flowaccumulator as fa
import gen_merge
from constants import *

args = [BASINCSV, RUNOFFCSV, CONSUMPTIONCSV, BACSV]

def f0(i, r, *args):
    return r[i,:]

def f(i, idx, values, r, uc, *args):
    # compute values - uc for each upstream basin (row) for all years (columns), sum by column
    x = np.sum(np.maximum(values[idx,:]-np.column_stack((uc[idx],)),0),0)
    return x + f0(i, r)

def main(basin_csv, r_csv, uc_csv, ba_csv):
    basin_rec = mlab.csv2rec(basin_csv)

    uc_rec = mlab.csv2rec(uc_csv)
    r_rec = mlab.csv2rec(r_csv)

    ids = basin_rec["basinid"]
    d_ids = basin_rec["dwnbasinid"]
 
    uc = gen_merge.arrange_vector_by_ids(uc_rec["ct"],uc_rec["basinid"],ids)

    n = len(ids)
    yrs = len(r_rec.dtype)-1
    
    ba = np.ones((n, yrs+1)) * NULL_VALUE
    ba[:,0] = ids 
   
    r = np.zeros((n,yrs))
    for i in range(yrs):
        yr = r_rec.dtype.names[i+1]
        r[:,i] = gen_merge.arrange_vector_by_ids(r_rec[yr],r_rec["basinid"],ids)
    
    ba[:,1:]= fa.accumulate_vector(ids, d_ids, f0, f, yrs, r, uc)
    
    outrec = np.rec.fromarrays(ba.transpose(),names=r_rec.dtype.names)
    
    mlab.rec2csv(outrec, ba_csv)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1:])
    else:
        main(*args)

