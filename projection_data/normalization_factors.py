
import pandas as pd
import numpy as np
import os

baseline_file = "csvs/baseline_20141116.csv"
ut_file = "csvs/Summary-20140630.csv"

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
CTt = '2010'
CTb = 'CT'
ROt = '1980'
ROb = 'RO'
UTt = 'Ut_2010_'
UTb = 'UT'

OUTDIR = 'csvs/'


def diff_ct(s,m,r):
    incsv = os.path.join(OUTDIR,"ct_%s_%s_%s.csv"%(s,m,r))
    dft = pd.read_csv(incsv)
    dfb = pd.read_csv(baseline_file)
    facdf = dfb[CTb]-dft[CTt]
    
    corrdf = dft.add(facdf,0)
    corrdf[corrdf<0] = 0
    
    facdf.to_csv(os.path.join(OUTDIR,"ct_fac_%s_%s_%s.csv"%(s,m,r)))
    corrdf.to_csv(os.path.join(OUTDIR,"ct_corr_%s_%s_%s.csv"%(s,m,r)))
    print "ct_corr_%s_%s_%s.csv"%(s,m,r)

def diff_ro(s,m,r):
    incsv = os.path.join(OUTDIR,"ro_base_%s_%s_%s.csv"%(m,s,r))
    dft = pd.read_csv(incsv)
    dfb = pd.read_csv(baseline_file)
    facdf = dfb[ROb]-dft[ROt]
    
    corrdf = dft.add(facdf,0)
    corrdf[corrdf<0] = 0
    
    facdf.to_csv(os.path.join(OUTDIR,"ro_fac_%s_%s_%s.csv"%(m,s,r)))
    corrdf.to_csv(os.path.join(OUTDIR,"ro_corr_%s_%s_%s.csv"%(m,s,r)))
    print "ro_corr_%s_%s_%s.csv"%(m,s,r)

def diff_ut(s):
    dft = pd.read_csv(ut_file)
    dfb = pd.read_csv(baseline_file)
    facdf = dfb[UTb]-dft['Ut_2010_%s'%s]
    
    corrdf = pd.DataFrame()
    for i in [2010,2020,2030,2040]:
        corrdf[i] = dft['Ut_%s_%s'%(i,s)]
    corrdf = corrdf.add(facdf,0)
    corrdf[corrdf<0] = 0
    
    facdf.to_csv(os.path.join(OUTDIR,"ut_fac_%s.csv"%(s)))
    corrdf.to_csv(os.path.join(OUTDIR,"ut_corr_%s.csv"%(s)))
    print "ut_corr_%s.csv"%(s)

def main():
    for i in range(len(rcpssps)):
        j = (i>0)
        for m in mdls[j]:
            for r in mdls[j][m]:
                diff_ct(rcpssps[i],m,r)
                if i==j:
                    diff_ro(rcps[i],m,r)
        diff_ut(rcpssps[i])



if __name__=="__main__":
    main()
