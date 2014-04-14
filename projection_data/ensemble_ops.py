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

SFX = '_m-20140402'
ANNUAL = 'annual/'
MONTHLY = 'monthly/'

def csv_BT(t, mdl, rcp, run, pfx='', sfx='', **kwargs):
    if t <= HISTORICAL:
        p = '%s%s_historical_%s' % (pfx, mdl, run)
    else:
        p = '%s%s_%s_%s' % (pfx, mdl, rcp, run)
    return pd.read_csv("%s_%s%s.csv" % (p, t, sfx))[BT]

def moving_average(maf, syear=1980, eyear=2090, window=21, **kwargs):
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

def iter_models(f, **kwargs):
    li = []
    for s in range(len(rcps)):
        for mdl,rs in mdls[s].iteritems():
            for r in rs:
                li.append(f(mdl=mdl, rcp=rcps[s], run=r, **kwargs))
    return li

def mdl_weights(rcp):
    weights = []
    w = 1.0/len(mdls[rcp])
    for mdl in mdls[rcp].itervalues():
        weights.extend([w / len(mdl) for _ in range(len(mdl))])
    return weights

def dump_stats(mdl_list, pfx=''):
    rcpidx = 0
    for s in range(len(rcps)):
        w = mdl_weights(s)
        mean = mdl_list[rcpidx]*w[0]
        for i in range(1,len(w)):
            mean += mdl_list[i+rcpidx]*w[i]
        mean.to_csv("%s_mean_%s.csv" % (pfx, rcps[s]))
        print("%s_mean_%s.csv" % (pfx, rcps[s]))
        
        var = ((mdl_list[rcpidx]-mean)**2)*w[0]
        for i in range(1,len(w)):
            var += ((mdl_list[i+rcpidx]-mean)**2)*w[i]
        sd = np.sqrt(var)
        sd.to_csv("%s_sd_%s.csv" % (pfx, rcps[s]))
        print("%s_sd_%s.csv" % (pfx, rcps[s]))

        cv = sd/mean
        cv.to_csv("%s_cv_%s.csv" % (pfx, rcps[s]))
        print("%s_cv_%s.csv" % (pfx, rcps[s]))

        rcpidx += len(w)
    

def annual_stats():
    all_mdls = iter_models(moving_average, maf=csv_BT, pfx=ANNUAL, sfx=SFX)
    dump_stats(all_mdls, 'bt')

def annual_var():
    all_mdls = iter_models(interannual_cv, maf=csv_BT, pfx=ANNUAL, sfx=SFX)
    dump_stats(all_mdls, 'iav')

def seasonal_stats():
    all_mdls = iter_models(moving_average, maf=intraannual_cv, yrf=csv_BT, pfx=MONTHLY, sfx=SFX)
    dump_stats(all_mdls, 'sv')


def main():
    annual_stats()
    annual_var()
    seasonal_stats()


if __name__ == "__main__":
    main()
