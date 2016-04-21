
import pandas as pd
import matplotlib.pyplot as pl
import os
import numpy as np

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

rcps = ['rcp45','rcp85']

OUTDIR = 'csvs'
ROW1 = 10587 #potomac
ROW2 = 11610 #colorado river

tBtch   = 'bt_ch_{}_{}_{}.csv'
tBtmch   = 'bt_mean_ch_{}.csv'
AREA = 'csvs/basin_area_20140121.csv'

def loadData(i):
    incsv = os.path.join(OUTDIR,tBtmch.format(rcps[i]))
    df = pd.read_csv(incsv)
    df['basin_id'] = np.arange(15006)+1
    df.set_index('basin_id', inplace=True)
    wdf = pd.read_csv(AREA)
    wdf.set_index('BasinID', inplace=True)
    df = df.join(wdf)
    df.dropna(inplace=True)
    return df

def main():
    for j in range(len(rcps)):
        arr = loadData(j)
        print arr.dtypes
        x = np.log(np.asarray(arr['2040']))
        w = np.asarray(arr['F_AREA'])
        pl.hist(x, weights=w, bins=25, range=(-.5,.5), normed=True, linewidth=0)
        pl.yticks([1,2,3,4,5])
        pl.xticks([-.5,-.25,0,.25,.5])
        pl.savefig('change_{}.pdf'.format(rcps[j]))
        pl.figure()
        
    '''
    for j in range(len(rcps)):
        arr = loadData(j,ROW1)
        for i in range(len(arr)):
            pl.plot(arr[i])
        pl.title("Washington DC (Potomac River) change in runoff " + rcps[j])
        pl.ylabel("Volume")
        pl.xlabel("Years past 1960")
        pl.show()
        pl.figure()

    for j in range(len(rcps)):
        arr = loadData(j,ROW2)
        for i in range(len(arr)):
            pl.plot(arr[i])
        pl.title("Texan Colorado River change in runoff " + rcps[j])
        pl.ylabel("Volume")
        pl.xlabel("Years past 1960")
        pl.show()
        pl.figure()
    '''

if __name__ == "__main__":
    main()



