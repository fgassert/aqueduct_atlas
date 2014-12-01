import pandas as pd
import numpy as np
import sys
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
HISTORICAL = 2005
BT = 'Bt'
RO = 'RO'
CT = 'Ct'

SFX = '_m-20140402'
ANNUAL = 'annual/'
MONTHLY = 'monthly/'
OUTDIR = 'csvs/'

def csv_BT(t, mdl, rcp, run, pfx='', sfx='', **kwargs):
    if t <= HISTORICAL:
        p = '%s%s_historical_%s' % (pfx, mdl, run)
    else:
        p = '%s%s_%s_%s' % (pfx, mdl, rcp, run)
    return pd.read_csv("%s_%s%s.csv" % (p, t, sfx))[BT]

def csv_RO(t, mdl, rcp, run, pfx='', sfx='', **kwargs):
    if t <= HISTORICAL:
        p = '%s%s_historical_%s' % (pfx, mdl, run)
    else:
        p = '%s%s_%s_%s' % (pfx, mdl, rcp, run)
    return pd.read_csv("%s_%s%s.csv" % (p, t, sfx))[RO]

def moving_average(maf, syear=1960, eyear=2090, window=21, **kwargs):
    outdf = pd.DataFrame()
    nyears = eyear-syear+1
    
    indf = maf(t=syear,**kwargs)
    years = np.empty((len(indf),eyear-syear+1))
    years[:,0] = indf    
    for yr in range(1,nyears):
        indf = maf(t=yr+syear,**kwargs)
        years[:,yr] = indf
        if yr >= window-1:
            outdf[syear+yr-window//2] = np.mean(years[:,yr-window+1:yr+1],1)
    return outdf

def interannual_cv(maf, syear=1980, eyear=2090, window=21, **kwargs):
    outdf = pd.DataFrame()
    nyears = eyear-syear+1
    
    indf = maf(t=syear,**kwargs)
    years = np.empty((len(indf),eyear-syear+1))
    years[:,0] = indf    
    for yr in range(1,nyears):
        indf = maf(t=yr+syear,**kwargs)
        years[:,yr] = indf
        if yr >= window-1:
            outdf[syear+yr-window//2] = np.std(years[:,yr-window+1:yr+1],1)/np.mean(years[:,yr-window+1:yr+1],1)
    return outdf

def intraannual_cv(yrf, t=1990, sfx='', **kwargs):
    indf = yrf(t=t, sfx="%0.2d%s"%(1,sfx), **kwargs)
    months = np.empty((len(indf),12))
    months[:,0]=indf
    for m in range(1,12):
        indf = yrf(t=t, sfx="%0.2d%s"%(m+1,sfx), **kwargs)
        months[:,m]=indf
        
    means = np.mean(months,1)
    sds = np.std(months,1)
    cvs = sds/means

    return cvs

def iter_models(f, dump=None, **kwargs):
    li = []
    for s in range(len(rcps)):
        for mdl,rs in mdls[s].iteritems():
            for r in rs:
                li.append(f(mdl=mdl, rcp=rcps[s], run=r, **kwargs))
                if dump is not None:
                    o = os.path.join(OUTDIR,"%s_%s_%s_%s.csv" % 
                                     (dump,rcps[s],mdl,r))
                    li[-1].to_csv(o)
                    print o
    return li

def annual_stats():
    hist = iter_models(moving_average, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='bt_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(moving_average, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='bt')

def annual_var():
    hist = iter_models(interannual_cv, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='iav_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(interannual_cv, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='iav')

def seasonal_stats():
    hist = iter_models(moving_average, maf=intraannual_cv, yrf=csv_BT, pfx=MONTHLY, sfx=SFX, dump='sv_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(moving_average, maf=intraannual_cv, yrf=csv_BT, pfx=MONTHLY, sfx=SFX, dump='sv')

def main():
    annual_ro()
    #annual_var()
    seasonal_stats()

if __name__ == "__main__":
    main()
