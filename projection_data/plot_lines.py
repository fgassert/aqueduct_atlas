
import pandas as pd
import matplotlib.pyplot as pl
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

rcps = ['rcp45','rcp85']

OUTDIR = 'csvs'
ROW1 = 10587 #potomac
ROW2 = 11610 #colorado river

def loadData(i,row):
    arr = []
    for m in mdls[i]:
        for r in mdls[i][m]:
            incsv = os.path.join(OUTDIR,"ro_%s_%s_%s.csv"%(m,rcps[i],r))
            df = pd.read_csv(incsv)
            arr.append(df.loc[row][1:])
    return arr

def main():
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

if __name__ == "__main__":
    main()



