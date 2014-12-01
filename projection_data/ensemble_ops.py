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

def mdl_weights(rcp):
    weights = []
    w = 1.0/len(mdls[rcp])
    for mdl in mdls[rcp].itervalues():
        weights.extend([w / len(mdl) for _ in range(len(mdl))])
    return weights

def dump_stats(mdl_list, pfx=''):
    rcpidx = 0
    for s in range(len(rcps)):
        w = np.matrix(mdl_weights(s)*np.ones((len(mdl_list[rcpidx]),1)))
        mean = np.zeros(mdl_list[rcpidx].shape)
        for i in range(0,w.shape[1]):
            n = np.isnan(mdl_list[i+rcpidx])
            mdl_list[i+rcpidx][n] = 0
            w[:,i][np.any(n,1)] = 0
            mean += np.multiply(mdl_list[i+rcpidx],w[:,i])
        mean = np.divide(mean,np.sum(w,1))
        meandf = pd.DataFrame(mean, columns=mdl_list[rcpidx].columns)
        meandf.to_csv(os.path.join(OUTDIR,"%s_mean_%s.csv" % (pfx, rcps[s])))
        print("%s_mean_%s.csv" % (pfx, rcps[s]))
        
        rows = mdl_list[rcpidx].shape[0]
        diff = np.zeros((rows*w.shape[1],mdl_list[rcpidx].shape[1]))
        for i in range(0,w.shape[1]):
            diff[i*rows:(i+1)*rows] = (mdl_list[i+rcpidx]-mean)/mean
        diffdf = pd.DataFrame(diff, columns=mdl_list[rcpidx].columns)
        diffdf.to_csv(os.path.join(OUTDIR,"%s_diff_%s.csv" % (pfx, rcps[s])))
        print("%s_diff_%s.csv" % (pfx, rcps[s]))

        var = np.zeros(mdl_list[rcpidx].shape)
        for i in range(0,w.shape[1]):
            v = np.multiply(((mdl_list[i+rcpidx]-mean)**2),w[:,i])
            var += v
        var = np.divide(var,np.sum(w,1))
        sd = np.sqrt(var)
        sddf = pd.DataFrame(sd, columns=mdl_list[rcpidx].columns)
        sddf.to_csv(os.path.join(OUTDIR,"%s_sd_%s.csv" % (pfx, rcps[s])))
        print("%s_sd_%s.csv" % (pfx, rcps[s]))

        cv = pd.DataFrame(sd/mean, columns=mdl_list[rcpidx].columns)
        cv.to_csv(os.path.join(OUTDIR,"%s_cv_%s.csv" % (pfx, rcps[s])))
        print("%s_cv_%s.csv" % (pfx, rcps[s]))

        rcpidx += w.shape[1]


def annual_stats():
    hist = iter_models(moving_average, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='bt_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(moving_average, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='bt')
    #dump_stats(all_mdls, 'bt')

def annual_ro():
    hist = iter_models(moving_average, maf=csv_RO, pfx=ANNUAL, sfx=SFX, dump='ro_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(moving_average, maf=csv_RO, pfx=ANNUAL, sfx=SFX, window=21, dump='ro')
    #dump_stats(all_mdls, 'ro')

def annual_var():
    hist = iter_models(interannual_cv, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='iav_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(interannual_cv, maf=csv_BT, pfx=ANNUAL, sfx=SFX, dump='iav')
    #dump_stats(all_mdls, 'iav')

def seasonal_stats():
    hist = iter_models(moving_average, maf=intraannual_cv, yrf=csv_BT, pfx=MONTHLY, sfx=SFX, dump='sv_base', syear=1950, eyear=2010, window=61)
    all_mdls = iter_models(moving_average, maf=intraannual_cv, yrf=csv_BT, pfx=MONTHLY, sfx=SFX, dump='sv')
    #dump_stats(all_mdls, 'sv')


def main():
    #annual_ro()
    #annual_stats()
    #annual_var()
    seasonal_stats()

if __name__ == "__main__":
    main()
