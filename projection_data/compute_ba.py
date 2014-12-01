
import pandas as pd
import numpy as np
import flowaccumulator as fa
import os

mdls = [
    {
        'CCSM4':['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i1p1','r6i1p1'],
        'CNRM-CM5':['r1i1p1'],
        'GFDL-ESM2M':['r1i1p1'],
        'MPI-ESM-LR':['r1i1p1','r2i1p1','r3i1p1'],
        'MRI-CGCM3':['r1i1p1'],
        'inmcm4':['r1i1p1']
    },
    {
        'CCSM4':['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i1p1','r6i1p1'],
        'CNRM-CM5':['r1i1p1','r2i1p1','r4i1p1','r6i1p1'],
        'GFDL-ESM2M':['r1i1p1'],
        'MPI-ESM-LR':['r1i1p1','r2i1p1','r3i1p1'],
        'MRI-CGCM3':['r1i1p1'],
        'inmcm4':['r1i1p1']
    }]

rcpssps = ['RCP45_SSP2','RCP85_SSP2','RCP85_SSP3']
rcps = ['rcp45','rcp85']

BASINCSV = 'csvs/basins_15006.csv'

OUTDIR = 'csvs/'
TYEARS = [2010,2020,2030,2040]
WINDOW = 21

BASINID = 'BasinID'
DWNBASIN = 'dwnBasinID'

def main():

    basin_arr = pd.read_csv(BASINCSV)
    ids = basin_arr[BASINID]
    d_ids = basin_arr[DWNBASIN]
    
    def f0( i, r, *args):
        return r[i]
    def f( i, idx, values, r, ct, *args):
        return np.sum(np.fmax(values[idx]-ct[idx],0),0) + f0(i, r)

    for i in range(len(rcpssps)):
        j = (i>0)
        for m in mdls[j]:
            for r in mdls[j][m]:
                incsv = os.path.join(OUTDIR,"ct_%s_%s_%s.csv"%(rcpssps[i],m,r))
                ct = pd.read_csv(incsv)
                incsv = os.path.join(OUTDIR,"ro_%s_%s_%s.csv"%(m,rcps[j],r))
                ro = pd.read_csv(incsv)
                for y in TYEARS:
                    if y == 2010:
                        ro_arr = np.asarray(pd.read_csv(os.path.join(OUTDIR,"ro_base_%s_%s_%s.csv"%(m,rcps[j],r)))['1980'])
                    else:
                        ro_arr = np.asarray(ro[str(y)])
                    c_arr = np.asarray(ct[str(y)])
                    ba = fa.accumulate(ids,d_ids,f0,f,ro_arr,c_arr)
                    outdf = pd.DataFrame()
                    outdf[BASINID]=ids
                    outdf['BA'] = ba
                    outdf.set_index(BASINID)
                    out = os.path.join(OUTDIR,"ba_%s_%s_%s_%s.csv"%(rcpssps[i],m,r,y))
                    outdf.to_csv(out)
                    print out

if __name__ == "__main__":
    main()
