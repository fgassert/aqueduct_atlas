
import pandas as pd
import numpy as np
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
TYEAR = [2010,2020,2030,2040]
HISTORICAL = 2005
WINDOW = 21

OUTDIR = 'csvs/ct/'



def rename_csvs():
    for y in TYEAR:
        for i in range(len(rcpssps)):
            j = (i>0)
            for m in mdls[j]:
                for r in mdls[j][m]:
                    for t in range(y-WINDOW//2,y+(WINDOW+1)//2):
                        rename_csv(y,rcpssps[i],m,r,t)
            
def rename_csv(tyear,rcp_ssp,mdl,run,t):
    if t <= HISTORICAL:
        rcp = 'historical'
    else:
        rcp = rcp_ssp[:5].lower()
    incsv = os.path.join("ct",
                       "%s_%s-20140630"%(tyear,rcp_ssp),
                       "%s_%s"%(mdl,run),
                       "output",
                       "%s_%s_%s_%s_m.csv"%(mdl,rcp,run,t))
    outcsv = os.path.join("ct-20140630",
                          "ct_%s_%s_%s_%s_%s_m.csv"%(rcp_ssp,tyear,mdl,run,t))
    os.rename(incsv,outcsv)
    print incsv,outcsv

def read_ct(tyear,rcp_ssp,mdl,run,t):
    csv = os.path.join("ct-20140630",
                       "ct_%s_%s_%s_%s_%s_m.csv"%(rcp_ssp,tyear,mdl,run,t))
    return pd.read_csv(csv)['Ct']

def tyear_average(tyears,window,rcp_ssp,mdl,run):
    outdf = pd.DataFrame()
    for tyear in tyears:
        syear = tyear-window//2
        eyear = tyear+(window+1)//2
        indf = read_ct(tyear,rcp_ssp,mdl,run,syear)
        years = np.empty((len(indf),eyear-syear+1))
        years[:,0] = indf
        for t in range(syear+1,eyear):
            indf = read_ct(tyear,rcp_ssp,mdl,run,t)
            years[:,t-syear] = indf
            outdf[tyear] = np.mean(years,1)
    return outdf

def main():
    #rename_csvs()
    for i in range(len(rcpssps)):
        j = (i>0)
        for m in mdls[j]:
            for r in mdls[j][m]:
                df = tyear_average(TYEAR,WINDOW,rcpssps[i],m,r)
                out = os.path.join(OUTDIR,
                                   "ct_%s_%s_%s.csv"%(rcpssps[i],m,r))
                df.to_csv(out)
                print out

if __name__=="__main__":
    main()
