
import pandas as pd
import numpy as np
import os
import flowaccumulator as fa
import fiona_join as fjoin

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

RCPSSP = ['RCP45_SSP2','RCP85_SSP2','RCP85_SSP3']
RCP = ['rcp45','rcp85']
SRES = {0:'B2',1:'B2',2:'A2'}
YRS = ['2010','2020','2030','2040']
BASEYR = '2010'

OUTDIR = 'csvs/'

# template strings for filenames
tRo21yr = 'ro_{}_{}_{}.csv'
tRobase = 'ro_base_{}_{}_{}.csv'
tRocorr = 'ro_corr_{}_{}_{}.csv'
tCt     = 'ct_{}_{}_{}.csv'
tCtcorr = 'ct_corr_{}_{}_{}.csv'
tBa     = 'ba_{}_{}_{}.csv'
tBacorr = 'ba_corr_{}_{}_{}.csv'
tBt     = 'bt_{}_{}_{}.csv'
tBtcorr = 'bt_corr_{}_{}_{}.csv'
tBtch   = 'bt_ch_{}_{}_{}.csv'
tWs     = 'ws_{}_{}_{}.csv'
tWscorr = 'ws_corr_{}_{}_{}.csv'
tWsch   = 'ws_ch_{}_{}_{}.csv'
tSv     = 'sv_{}_{}_{}.csv'
tSvbase = 'sv_base_{}_{}_{}.csv'
tSvcorr = 'sv_corr_{}_{}_{}.csv'
tSvch   = 'sv_ch_{}_{}_{}.csv'

tUt     = 'ut_{}.csv'
tUtcorr = 'ut_corr_{}.csv'
tUtch   = 'ut_ch_{}.csv'

tCtm     = 'ct_mean_{}.csv'
tBam     = 'ba_mean_{}.csv'
tBacorrm = 'ba_corr_mean_{}.csv'
tBtm     = 'bt_mean_{}.csv'
tBtmch   = 'bt_mean_ch_{}.csv'
tBtcorrm = 'bt_corr_mean_{}.csv'
tBtcv    = 'bt_cv_{}.csv'
tSvm     = 'sv_mean_{}.csv'
tSvcorrm = 'sv_corr_mean_{}.csv'
tSvcv    = 'sv_cv_{}.csv'
tSvmch   = 'sv_mean_ch_{}.csv'
tWsm     = 'ws_mean_{}.csv'
tWscorrm = 'ws_corr_mean_{}.csv'
tWsmch   = 'ws_mean_ch_{}.csv'

tUtvsBt  = 'ut_vs_bt_{}.csv'
tPop     = '{}pa{}_5min.csv'
tPopsum  = 'popsum_{}.csv'

tIv      = 'iav_{}_{}_{}.csv'
tIvbase  = 'iav_base_{}_{}_{}.csv'
tIvch    = 'iav_ch_{}_{}_{}.csv'
tIvm     = 'iav_mean_{}.csv'
tIvcv    = 'iav_cv_{}.csv'
tIvmch   = 'iav_mean_ch_{}.csv'


UTCSV = "Summary-20140630.csv"
UTTEMPLATE = 'Ut_{}_{}'

BASELINE = 'baseline_20141116.csv'
#baseline column names
bCT = 'CT'
bRO = 'RO'
bUT = 'UT'
bSV = 'SV'

BASINCSV = 'basins_15006.csv'
AREACSV = "basin_area_20140121.csv"
AREAM2 = "F_AREA"
LABELS = "labels_20140416.csv"

INDIR = 'csvs/'
BASINID = 'BasinID'
DWNBASIN = 'dwnBasinID'
NROWS = 15006
LARGE_NUMBER = 1e16
CHANGECATEGORIES = 7

II = ['ws','ut','bt','sv']
YY = ['20','30','40']
SS = ['24','28','38']
R = ['t','c','u']

DUMPCSV = "prepped.csv"

INSHP = "shps/Basins_15006-20130820.shp"
OUTSHP = "shps/out.shp"

EXTRACSV = "figs.csv"
EXTRASHP = "shps/figs.shp"

__csvs = {}
def readArr(fname,cols=None,cache=False,in_dir=INDIR,sort_index=BASINID,nrows=NROWS):
    """
    attemps to load and cache named csv into numpy array, 
    sorts by and drops basinid, 
    optionally selects columns
    """
    if fname in __csvs:
        df = __csvs[fname]
    else:
        df = pd.read_csv(os.path.join(in_dir,fname))
        if sort_index in df.columns:
            df.sort(sort_index,inplace=True)
            df.reset_index()
            df.drop(sort_index,1,inplace=True)
        if 'Unnamed: 0' in df.columns: df.drop('Unnamed: 0',1,inplace=True)
        if len(df) != nrows: print "warning: incorrect csv length: %s, %s" % (fname,len(df))
        if cache:
            __csvs[fname] = df
        else: dropArr(fname)
    if cols is not None:
        return df[cols].values
    return df.values
def readLabels(fname,in_dir=INDIR,sort_index=BASINID):
    if fname in __csvs:
        df = __csvs[fname]
    else:
        df = pd.read_csv(os.path.join(in_dir,fname))
    labels = df.columns
    if sort_index in labels: labels = labels.drop(sort_index)
    if 'Unnamed: 0' in labels: labels = labels.drop('Unnamed: 0')
    return labels

def dropArr(fname):
    if fname in __csvs:
        del __csvs[fname]
def dumpDF(df,fname,nrows=NROWS):
    if len(df) != nrows: print "warning: incorrect csv length: %s, %s" % (fname,len(df))
    df.to_csv(os.path.join(OUTDIR,fname),index=False)
    print fname

def fSMR(fname,s,m,r):
    return fname.format(s,m,r)

def weighted_mean(s, j, tname, meanfile=None, sdfile=None, cvfile=None):
    '''
    compute weighted ensemble mean & cv given a template filename
    '''
    #init weights and arrays
    weights  = []
    arr_list = []
    labels = None
    w1 = 1.0/len(mdls[j])
    for m,rs in mdls[j].iteritems():
        for r in rs:
            weights.append(w1/len(rs))
            arr_list.append(readArr(fSMR(tname,s,m,r)))
            if labels is None:
                labels = readLabels(fSMR(tname,s,m,r))

    w = np.matrix(weights*np.ones((NROWS,1)))

    mean = np.zeros(arr_list[0].shape)
    for x in range(0,w.shape[1]):
        n = np.isnan(arr_list[x])
        arr_list[x][n] = 0
        w[:,x][np.any(n,1)] = 0
        mean += np.multiply(arr_list[x],w[:,x])
    mean = np.divide(mean,np.sum(w,1))
    
    if meanfile is not None:
        meandf = pd.DataFrame(mean, columns=labels)
        dumpDF(meandf, meanfile.format(s))
    
    if sdfile is not None or cvfile is not None:
        var = np.zeros(arr_list[0].shape)
        for x in range(0,w.shape[1]):
            v = np.multiply(np.square(arr_list[x]-mean),w[:,x])
            var += v
        var = np.divide(var,np.sum(w,1))
        sd = np.sqrt(var)
        if sdfile is not None:
            sddf = pd.DataFrame(sd, columns=labels)
            dumpDF(sddf, sdfile.format(s))
        if cvfile is not None:
            #for purposes of uncert measurement increase cv for missing values
            cv = np.divide(sd/mean,np.sum(w,1))
            cvdf = pd.DataFrame(cv, columns=labels)
            dumpDF(cvdf, cvfile.format(s))

def get_change_thresholds(n=9,base=2,rate=.25):
    t = base**(np.arange(n)*rate-(n-2)*rate/2)
    t[-1] = LARGE_NUMBER
    return t
def get_mask_thresholds(n=2,base=2,rate=.25):
    return base**((np.arange(n)+1)*rate)-1
def get_log_thresholds(n=5,base=2,start=.1):    
    t = base**np.arange(n)*start
    t[-1] = LARGE_NUMBER
    return t
def get_linear_thresholds(n=5,base=.33,start=.33):    
    t = base*np.arange(n)+start
    t[-1] = LARGE_NUMBER
    return t
def threshold_score(vec, thresholds):
    return np.sum(vec > thresholds[:,np.newaxis],0)



def F_ut(s):
    """
    bymodel:
    in: ut_unformatted
    out: ut
    """
    ut = pd.DataFrame()
    for y in YRS:
        ut[y] = readArr(UTCSV,UTTEMPLATE.format(y,s),True)
    dumpDF(ut,tUt.format(s))
    #cleanup
    dropArr(UTCSV)
def Sub_ut_corr(s):
    """
    bymodel:
    in: ut, ut_gldas
    out: ut_corr
    """
    utbase = readArr(tUt.format(s),[BASEYR],True) #as columns
    utgldas = readArr(BASELINE,[bUT],True)
    arr = np.empty((NROWS,len(YRS)),np.double)    
    diff = utbase-utgldas
    arr[:,0] = utgldas.ravel()
    arr[:,1:] = np.fmax(readArr(tUt.format(s),YRS[1:])+diff,0)
    utcorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(utcorr,tUtcorr.format(s))
def Div_ut_ch(s):
    """
    bymodel:
    in: ut
    out: ut_ch
    """
    ut_base = readArr(tUt.format(s),[BASEYR],True)
    ut = readArr(tUt.format(s),YRS[1:])
    arr = ut/ut_base
    ut_ch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(ut_ch,tUtch.format(s))

def Sub_ct_corr(s,m,r):
    """
    bymodel:
    in: ct_base, ct_21yr, ct_gldas
    out: ct_corr
    """
    ctbase = readArr(fSMR(tCt,s,m,r),[BASEYR],True) #treat as column
    ctgldas = readArr(BASELINE,[bCT],True)
    arr = np.empty((NROWS,len(YRS)),np.double)
    diff = ctgldas-ctbase
    arr[:,0] = ctgldas.ravel()
    arr[:,1:] = np.fmax(readArr(fSMR(tCt,s,m,r),YRS[1:])+diff,0)
    ctcorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(ctcorr,fSMR(tCtcorr,s,m,r))
def Sub_ro_corr(s,m,r):
    """
    bymodel:
    in: ro_base, ro_21yr, ro_gldas
    out: ro_corr
    """
    robase = readArr(fSMR(tRobase,s,m,r))
    rogldas = readArr(BASELINE,[bRO],True)
    arr = np.empty((NROWS,len(YRS)),np.double)
    diff = rogldas-robase
    arr[:,0] = rogldas.ravel()
    arr[:,1:] = np.maximum(readArr(fSMR(tRo21yr,s,m,r),YRS[1:])+diff,0)
    rocorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(rocorr,fSMR(tRocorr,s,m,r))

def f0( i, r, *args):
    return r[i]
def ba_f( i, idx, values, r, ct, *args):
    return np.sum(np.fmax(values[idx]-ct[idx],0),0) + f0(i, r)
def FA_ba(i,m,r):
    """
    bymodel:
    in: ro_21yr, ct
    out: ba
    """
    ids = np.arange(NROWS)+1
    d_ids = readArr(BASINCSV,DWNBASIN,True)
    ro = np.empty((NROWS,len(YRS)),dtype=np.double)
    ro[:,0] = readArr(fSMR(tRobase,RCP[i>0],m,r)).ravel()
    ro[:,1:] = readArr(fSMR(tRo21yr,RCP[i>0],m,r),YRS[1:])
    ro[np.isnan(ro)]=0
    ct = readArr(fSMR(tCt,RCPSSP[i],m,r),YRS)
    arr = fa.accumulate_vector(ids,d_ids,f0,ba_f,len(YRS),ro,ct)
    ba = pd.DataFrame(arr,columns=YRS)
    dumpDF(ba,fSMR(tBa,RCPSSP[i],m,r))
def FA_ba_corr(i,m,r):
    """
    bymodel:
    in: ro_corr, ct_corr
    out: ba_corr
    """
    ids = np.arange(NROWS)+1
    d_ids = readArr(BASINCSV,DWNBASIN,True)
    ro = readArr(fSMR(tRocorr,RCP[i>0],m,r),YRS)
    ct = readArr(fSMR(tCtcorr,RCPSSP[i],m,r),YRS)
    ro[np.isnan(ro)]=0
    arr = fa.accumulate_vector(ids,d_ids,f0,ba_f,len(YRS),ro,ct)
    ba = pd.DataFrame(arr,columns=YRS)
    dumpDF(ba,fSMR(tBacorr,RCPSSP[i],m,r))

def bt_f( i, idx, values, r, *args):
    return np.sum(values[idx],0) + f0(i, r)
def FA_bt(s,m,r):
    """
    bymodel:
    in: ro_21yr
    out: bt
    """
    ids = np.arange(NROWS)+1
    d_ids = readArr(BASINCSV,DWNBASIN,True)
    ro = np.empty((NROWS,len(YRS)),dtype=np.double)
    ro[:,0] = readArr(fSMR(tRobase,s,m,r)).ravel()
    ro[:,1:] = readArr(fSMR(tRo21yr,s,m,r),YRS[1:])
    ro[np.isnan(ro)]=0
    arr = fa.accumulate_vector(ids,d_ids,f0,bt_f,len(YRS),ro)
    bt = pd.DataFrame(arr,columns=YRS)
    dumpDF(bt,fSMR(tBt,s,m,r))
def FA_bt_corr(s,m,r):
    """
    bymodel:
    in: ro_corr
    out: bt_corr
    """
    ids = np.arange(NROWS)+1
    d_ids = readArr(BASINCSV,DWNBASIN,True)
    ro = readArr(fSMR(tRocorr,s,m,r),YRS)
    ro[np.isnan(ro)]=0
    arr = fa.accumulate_vector(ids,d_ids,f0,bt_f,len(YRS),ro)
    bt = pd.DataFrame(arr,columns=YRS)
    dumpDF(bt,fSMR(tBtcorr,s,m,r))
def Div_bt_ch(s,m,r):
    """
    bymodel:
    in: bt
    out: bt_ch
    """
    bt_base = readArr(fSMR(tBt,s,m,r),[BASEYR],True)
    bt = readArr(fSMR(tBt,s,m,r),YRS[1:])
    arr = bt/bt_base
    bt_ch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(bt_ch,fSMR(tBtch,s,m,r))

def Div_ws(s,m,r):
    """
    bymodel:
    in: ba, ut
    out: ws
    """
    ut = readArr(fSMR(tBa,s,m,r))
    ba = readArr(fSMR(tUt,s,m,r))
    arr = ut/ba
    ws = pd.DataFrame(arr,columns=YRS)
    dumpDF(ws,fSMR(tWs,s,m,r))
def Div_ws_corr(s,m,r):
    """
    bymodel:
    in: ba_corr, ut_corr
    out: ws_corr
    """
    ut = readArr(fSMR(tBacorr,s,m,r))
    ba = readArr(fSMR(tUtcorr,s,m,r))
    arr = ut/ba
    ws = pd.DataFrame(arr,columns=YRS)
    dumpDF(ws,fSMR(tWscorr,s,m,r))
def Div_ws_ch(s,m,r):
    """
    bymodel:
    in: ws
    out: ws_ch
    """
    ws_base = readArr(fSMR(tWs,s,m,r),[BASEYR],True)
    ws = readArr(fSMR(tWs,s,m,r),YRS[1:])
    arr = ws/ws_base
    ws_ch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(ws_ch,fSMR(tWsch,s,m,r))

def Div_sv_corr(s,m,r):
    """
    bymodel:
    in: sv_base, sv_21yr, sv_gldas
    out: sv_corr
    """
    svgldas = readArr(BASELINE,[bSV]) #as column
    svbase = readArr(fSMR(tSvbase,s,m,r))
    arr = np.empty((NROWS,len(YRS)),np.double)
    div = svgldas / svbase
    arr[:,0] = svgldas.ravel()
    arr[:,1:] = readArr(fSMR(tSv,s,m,r),YRS[1:])*div
    svcorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(svcorr,fSMR(tSvcorr,s,m,r))


def WA_ba_mean(i):
    '''
    in: ba bymodel
    out: ba_mean
    '''
    weighted_mean(RCPSSP[i],i>0,tBa,tBam)
def WA_ct_mean(i):
    '''
    in: ct bymodel
    out: ct_mean
    '''
    weighted_mean(RCPSSP[i],i>0,tCt,tCtm)
def WA_ba_corr_mean(i):
    '''
    in: ba_corr bymodel
    out: ba_corr_mean
    '''
    weighted_mean(RCPSSP[i],i>0,tBacorr,tBacorrm)
def WA_bt_mean_cv(j):
    '''
    in: bt bymodel
    out: bt_mean, bt_cv
    '''
    weighted_mean(RCP[j],j,tBt,tBtm,cvfile=tBtcv)
def WA_bt_corr_mean(j):
    '''
    in: bt_corr bymodel
    out: bt_corr_mean
    '''
    weighted_mean(RCP[j],j,tBtcorr,tBtcorrm)
def Div_bt_mean_ch(s):
    '''
    in: bt_mean
    out: bt_mean_ch
    '''
    btbase = readArr(tBtm.format(s),[BASEYR],True)
    bt = readArr(tBtm.format(s),YRS[1:])
    arr = bt/btbase
    btch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(btch,tBtmch.format(s))
def WA_sv_mean_cv(j):
    '''
    in: sv bymodel
    out: sv_mean, sv_cv
    '''
    weighted_mean(RCP[j],j,tSv,tSvm,cvfile=tSvcv)
def WA_sv_corr_mean(j):
    '''
    in: sv_corr bymodel
    out: sv_corr_mean
    '''
    weighted_mean(RCP[j],j,tSvcorr,tSvcorrm)
def Div_sv_mean_ch(s):
    '''
    in: sv_mean
    out: sv_mean_ch
    '''
    svbase = readArr(tSvm.format(s),[BASEYR],True)
    sv = readArr(tSvm.format(s),YRS[1:])
    arr = sv/svbase
    svch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(svch,tSvmch.format(s))

def WA_iv_mean_cv(j):
    '''
    in: iv bymodel
    out: iv_mean, iv_cv
    '''
    weighted_mean(RCP[j],j,tIv,tIvm,cvfile=tIvcv)
def Div_iv_mean_ch(s):
    '''
    in: iv_mean
    out: iv_mean_ch
    '''
    ivbase = readArr(tIvm.format(s),[BASEYR],True)
    iv = readArr(tIvm.format(s),YRS[1:])
    arr = iv/ivbase
    ivch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(ivch,tIvmch.format(s))


def Div_ws_mean(s):
    '''
    in: ut, ba_mean
    out: ws_mean
    '''
    ut = readArr(tUt.format(s),YRS)
    ba = readArr(tBam.format(s),YRS)
    arr = ut/ba
    ws = pd.DataFrame(arr,columns=YRS)
    dumpDF(ws,tWsm.format(s))
def Div_ws_corr_mean(s):
    '''
    in: ut_corr, ba_corr_mean
    out: ws_mean
    '''
    ut = readArr(tUtcorr.format(s),YRS)
    ba = readArr(tBacorrm.format(s),YRS)
    arr = ut/ba
    ws = pd.DataFrame(arr,columns=YRS)
    dumpDF(ws,tWscorrm.format(s))
def Div_ws_mean_ch(s):
    '''
    in: ws_mean
    out: ws_mean_ch
    '''
    wsbase = readArr(tWsm.format(s),[BASEYR],True)
    ws = readArr(tWsm.format(s),YRS[1:])
    arr = ws/wsbase
    wsch = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(wsch,tWsmch.format(s))

def Div_ut_vs_bt(i):
    '''
    in: ut_ch, bt_ch
    out: ut_vs_bt
    '''
    ut = readArr(tUtch.format(RCPSSP[i]),YRS[1:])
    bt = readArr(tBtmch.format(RCP[i>0]),YRS[1:])
    utmag = np.abs(np.log(ut))
    btmag = np.abs(np.log(bt))
    arr = utmag/(utmag+btmag)
    ws = pd.DataFrame(arr,columns=YRS[1:])
    dumpDF(ws,tUtvsBt.format(RCPSSP[i]))
def Sum_ws_pop(i):
    '''
    in: ws_mean, pop
    out: pop
    '''
    ws = readArr(tWsmch.format(RCPSSP[i]),YRS[1:])
    sumpop = pd.DataFrame()
    s = np.empty(len(YRS[1:]))
    wss = np.empty(len(YRS[1:]))
    for j in range(len(YRS)-1):
        pop = readArr(tPop.format(SRES[i],YRS[j+1]),['sum'])
        s[j] = np.nansum(pop)
        wss[j] = np.nansum(pop[ws[:,j]>2.0**0.25])
    sumpop['sum'] = s 
    sumpop['ws'] = wss
    sumpop['pct'] = wss/s
    dumpDF(sumpop,tPopsum.format(RCPSSP[i]))



def wst(s):
    '''
    in: ws_corr_mean, ba_corr_mean, ut_corr_mean, area
    out: wst
    '''
    raw = readArr(tWscorrm.format(s),YRS[1:])
    t = get_log_thresholds(5,2,.1)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    area = readArr(AREACSV,[AREAM2],True) #as column
    ba = readArr(tBacorrm.format(s),YRS[1:])
    ut = readArr(tUtcorr.format(s),YRS[1:])
    mask = (ut/area < 0.012) & (ba/area < 0.030)
    score[score == 5] = 6 #inf filter
    score[np.isnan(raw)] = 6
    score[mask] = 5
    labels = readArr(LABELS,'wst',True)[score]
    return raw, labels
def wsc(s):
    '''
    in: ws_mean_ch, ws_corr_mean
    out: wsc
    '''
    raw = readArr(tWsmch.format(s),YRS[1:])
    t = get_change_thresholds(CHANGECATEGORIES,2,rate=.5)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    ws = readArr(tWscorrm.format(s),YRS[1:])
    mask = ((ws <= .1) & (raw > 0)) | ((ws > .8) & (raw < 0))
    score[mask] = CHANGECATEGORIES//2
    score[np.isnan(raw)] = CHANGECATEGORIES
    labels = readArr(LABELS,'wsc',True)[score]
    return raw, labels
def wsu(s):
    '''
    in: none
    out: wsu
    '''
    raw = np.zeros((NROWS,len(YRS[1:])),dtype=int)
    labels = np.array(["N/A"])[raw]
    return raw,labels
def utt(s):
    '''
    in: ut_corr, area
    out: utt
    '''
    raw = readArr(tUtcorr.format(s),YRS[1:])/readArr(AREACSV,[AREAM2],True)
    t = get_log_thresholds(5,np.sqrt(10),.01)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    labels = readArr(LABELS,'utt',True)[score]
    return raw, labels
def utc(s):
    '''
    in: ut_ch,
    out: utc
    '''
    raw = readArr(tUtch.format(s),YRS[1:])
    t = get_change_thresholds(CHANGECATEGORIES, rate=.25)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    score[np.isnan(raw)] = CHANGECATEGORIES
    labels = readArr(LABELS,'utc',True)[score]
    return raw, labels
def utu(s):
    '''
    in: none
    out: utu
    '''
    raw = np.zeros((NROWS,len(YRS[1:])),dtype=int)
    labels = np.array(["N/A"])[raw]
    return raw,labels
def btt(s):
    '''
    in: bt_corr_mean, area
    out: btt
    '''
    raw = readArr(tBtcorrm.format(s),YRS[1:])/readArr(AREACSV,[AREAM2],True)
    t = get_log_thresholds(8,np.sqrt(10),.01)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    labels = readArr(LABELS,'btt',True)[score]
    return raw, labels
def btc(s):
    '''
    in: bt_mean_ch
    out: btc
    '''
    raw = readArr(tBtmch.format(s),YRS[1:])
    t = get_change_thresholds(CHANGECATEGORIES, rate=.25)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    score[np.isnan(raw)] = CHANGECATEGORIES
    labels = readArr(LABELS,'btc',True)[score]
    return raw, labels
def btu(s):
    '''
    in: bt_cv
    out: btu
    '''
    raw = readArr(tBtcv.format(s),YRS[1:])
    t = get_mask_thresholds(rate=.25)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    score[raw<1e-6] = 2 #if there's no variation something is wrong
    score[np.isnan(raw)] = 2 #if there's no variation something is wrong
    labels = readArr(LABELS,'btu',True)[score]
    return raw, labels
def svt(s):
    '''
    in: sv_corr_mean
    out: svt
    '''
    raw = readArr(tSvcorrm.format(s),YRS[1:])
    t = get_linear_thresholds(5,.33,.33)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    score[np.isnan(raw)] = 5
    score[raw==0] = 5
    labels = readArr(LABELS,'svt',True)[score]
    return raw, labels
def svc(s):
    '''
    in: sv_mean_ch
    out: svc
    '''
    raw = readArr(tSvmch.format(s),YRS[1:])
    t = get_change_thresholds(CHANGECATEGORIES, rate=.125)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    score[np.isnan(raw)] = CHANGECATEGORIES
    labels = readArr(LABELS,'svc',True)[score]
    return raw, labels
def svu(s):
    '''
    in: sv_cv
    out: svu
    '''
    raw = readArr(tSvcv.format(s),YRS[1:])
    t = get_mask_thresholds(rate=.125)
    score = np.empty((NROWS,len(YRS[1:])),int)
    for i in range(len(YRS[1:])):
        score[:,i] = threshold_score(raw[:,i], t)
    score[raw<1e-6] = 2 #if there's no variation something is wrong
    score[np.isnan(raw)] = 2 #if there's no variation something is wrong
    labels = readArr(LABELS,'svu',True)[score]
    return raw, labels


def generate_indicators():
    '''
    generates final indicator data frame and labels
    '''
    outdf = pd.DataFrame()
    outdf[BASINID] = np.arange(NROWS)+1

    generators = [
        [wst,wsc,wsu],
        [utt,utc,utu],
        [btt,btc,btu],
        [svt,svc,svu]
    ]
    
    for i in range(len(II)):
        for r in range(len(R)):
            for s in range(len(SS)):
                ss = RCPSSP[s]
                if i>1: ss=RCP[s>0] # no ssps for supply indicators
                raw, labels = generators[i][r](ss)
                for y in range(len(YY)):
                    outlblr = "{}{}{}{}r".format(II[i],YY[y],SS[s],R[r])
                    outlbll = "{}{}{}{}l".format(II[i],YY[y],SS[s],R[r])
                    outdf[outlblr] = raw[:,y]
                    outdf[outlbll] = labels[:,y]
    dumpDF(outdf,DUMPCSV)

def process_indicators():
    '''
    computes intermediate values for indicators
    '''
    '''
    for s in RCPSSP:
        F_ut(s)
        Sub_ut_corr(s)
        Div_ut_ch(s)
    
    for i in range(len(RCPSSP)):
        j = i>0
        for m,rs in mdls[j].iteritems():
            for r in rs:
                if i<2: 
                    ### MA_ro
                    ### MA_ro_base
                    ### MA_sv
                    ### MA_sv_base 
                    Sub_ro_corr(RCP[j],m,r)
                    FA_bt(RCP[j],m,r)
                    FA_bt_corr(RCP[j],m,r)
                    Div_bt_ch(RCP[j],m,r)
                    Div_sv_corr(RCP[j],m,r)
                ### MA_ct
                Sub_ct_corr(RCPSSP[i],m,r)
                FA_ba(i,m,r)
                FA_ba_corr(i,m,r)
                #Div_ws(RCPSSP[i],m,r)
                #Div_ws_corr(RCPSSP[i],m,r)
                #Div_ws_ch(RCPSSP[i],m,r)
    '''
    for j in range(len(RCP)):
        WA_bt_mean_cv(j)
        WA_bt_corr_mean(j)
        Div_bt_mean_ch(RCP[j])
        WA_sv_mean_cv(j)
        WA_sv_corr_mean(j)
        Div_sv_mean_ch(RCP[j])
        WA_iv_mean_cv(j)
        Div_iv_mean_ch(RCP[j])
    
    for i in range(len(RCPSSP)):
        WA_ct_mean(i)
        WA_ba_mean(i)
        WA_ba_corr_mean(i)
        Div_ws_mean(RCPSSP[i])
        Div_ws_corr_mean(RCPSSP[i])
        Div_ws_mean_ch(RCPSSP[i])
        Div_ut_vs_bt(i)
        Sum_ws_pop(i)

def gen_shape():
    c = os.path.join(OUTDIR,DUMPCSV)
    fjoin.joincsvtoshp(INSHP,BASINID,c,BASINID,OUTSHP)

def gen_extra_shape():
    outdf = pd.DataFrame()
    outdf[BASINID] = np.arange(NROWS)+1
    for s in range(len(RCPSSP)):
        for y in range(len(YY)):
            a = readArr(tUtvsBt.format(RCPSSP[s]),YRS[y+1])
            outdf['UtvsBt{}{}'.format(YY[y],SS[s])] = a
    dumpDF(outdf, EXTRACSV)
    c = os.path.join(OUTDIR,EXTRACSV)
    fjoin.joincsvtoshp(INSHP,BASINID,c,BASINID,EXTRASHP)

def main():
    process_indicators()
    generate_indicators()
    gen_shape()
    gen_extra_shape()


if __name__ == "__main__":
    main()
