
import pandas as pd
import numpy as np
import os
import flowaccumulator as fa

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
YRS = ['2010','2020','2030','2040']
BASEYR = '2010'

OUTDIR = 'csvs/'

# template strings for filenames
tRo21yr = 'ro_{}_{}_{}.csv'
tRobase = 'ro_base_{}_{}_{}.csv'
tRocorr = 'ro_corr_{}_{}_{}.csv'
tCt     = 'ct_{}_{}_{}.csv'
tCtcorr = 'ct_corr_{}_{}_{}.csv'
tUt     = 'ut_{}.csv'
tUtcorr = 'ut_corr_{}.csv'
tUtch   = 'ut_ch_{}.csv'
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

BASINCSV = 'basins_15006.csv'
UTCSV = "Summary-20140630.csv"
UTTEMPLATE = 'Ut_{}_{}'

BASELINE = 'baseline_20141116.csv'
#baseline column names
bCT = 'CT'
bRO = 'RO'
bUT = 'UT'
bSV = 'SV'

INDIR = 'csvs/'
BASINID = 'BasinID'
DWNBASIN = 'dwnBasinID'
NROWS = 15006

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
def dropArr(fname):
    if fname in __csvs:
        del __csvs[fname]
def dumpDF(df,fname,nrows=NROWS):
    if len(df) != nrows: print "warning: incorrect csv length: %s, %s" % (fname,len(df))
    df.to_csv(os.path.join(OUTDIR,fname),index=False)
    print fname


def fSMR(fname,s,m,r):
    return fname.format(s,m,r)
def combSMR():
    """ 
    generates a list with combinations of RCPSSP id, model name, and run name
    """
    li = []
    for i in range(len(RCPSSP)):
        j=(i>0)
        for m,rs in mdls[j].iteritems():
            for r in rs:
                li.append((i,m,r))
    return li


def F_ut(s):
    """
    bymodel:
    in: ut, ut_gldas
    out: ut_corr
    """
    ut = pd.DataFrame()
    for y in YRS:
        ut[y] = readArr(UTCSV,UTTEMPLATE.format(y,s),True)
    dumpDF(ut,tUt.format(s))
    #cleanup
    dropArr(UTCSV)
def Sub_ut_norm(s):
    """
    bymodel:
    in: ut, ut_gldas
    out: ut_corr
    """
    utbase = readArr(tUt.format(s),[BASEYR],True) #as columns
    utgldas = readArr(BASELINE,[bUT],True)
    arr = np.empty((NROWS,len(YRS)),np.double)    
    diff = utbase-utgldas
    arr[:,0] = utgldas
    arr[:,1:] = np.fmax(readArr(tUt.format(s),YRS[1:],True)+diff,0)
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

def Sub_ct_norm(s,m,r):
    """
    bymodel:
    in: ro_base, ro_21yr, ro_gldas
    out: ro_norm
    """
    ctbase = readArr(fSMR(tCt,s,m,r),[BASEYR],True) #treat as column
    ctgldas = readArr(BASELINE,[bCT],True)
    arr = np.empty((NROWS,len(YRS)),np.double)
    diff = ctgldas-ctbase
    arr[:,0] = ctgldas
    arr[:,1:] = np.fmax(readArr(fSMR(tCt,s,m,r),YRS[1:],True)+diff,0)
    ctcorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(ctcorr,fSMR(tCtcorr,s,m,r))
def Sub_ro_norm(s,m,r):
    """
    bymodel:
    in: ro_base, ro_21yr, ro_gldas
    out: ro_norm
    """
    robase = readArr(fSMR(tRobase,s,m,r))
    rogldas = readArr(BASELINE,[bRO],True)
    arr = np.empty((NROWS,len(YRS)),np.double)
    diff = rogldas-robase
    arr[:,0] = rogldas
    arr[:,1:] = np.fmax(readArr(fSMR(tRo21yr,s,m,r),YRS[1:],True)+diff,0)
    rocorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(rocorr,fSMR(tRocorr,s,m,r))

def f0( i, r, *args):
    return r[i]
def ba_f( i, idx, values, r, ct, *args):
    return np.sum(np.fmax(values[idx]-ct[idx],0),0) + f0(i, r)
def FA_ba(i,m,r,norm=False):
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
def FA_ba_norm(i,m,r):
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
def FA_bt_norm(s,m,r):
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
    dumpDF(bt,fSMR(tBt,s,m,r))
def Div_bt(s,m,r):
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
def Div_ws_norm(s,m,r):
    """
    bymodel:
    in: ba_norm, ut_norm
    out: ws_norm
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

def Div_sv_norm(s,m,r):
    """
    bymodel:
    in: sv_base, sv_21yr, sv_gldas
    out: sv_norm
    """
    svgldas = readArr(BASELINE,[bSV]) #as column
    svbase = readArr(fSMR(tSVbase,s,m,r))
    arr = np.empty((NROWS,len(YRS)),np.double)
    div = svgldas / svbase
    arr[:,0] = svgldas
    arr[:,1:] = readArr(fSMR(tSv,s,m,r),YRS[1:],True)*div
    svcorr = pd.DataFrame(arr,columns=YRS)
    dumpDF(svcorr,fSMR(tSvcorr,s,m,r))

def main():
    for s in RCPSSP:
        #F_ut(s)
        Sub_ut_norm(s)
        #Div_ut_ch(s)
        pass

    for i,m,r in combSMR():
        j = i>0
        #MA_ct
        Sub_ct_norm(RCPSSP[i],m,r)
        #MA_ro
        #MA_ro_base
        if i<2: 
            Sub_ro_norm(RCP[j],m,r)
        #FA_ba(i,m,r)
        #FA_ba_norm(i,m,r)
        #if i<2:
            #FA_bt(RCP[j],m,r)
            #FA_bt_norm(RCP[j],m,r)
            #Div_bt(RCP[j],m,r)
        #Div_ws(RCPSSP[i],m,r)
        #Div_ws_norm(RCPSSP[i],m,r)
        #Div_ws_ch(RCPSSP[i],m,r)
        if i<2:
            Sub_sv_norm(RCP[j],m,r)

if __name__ == "__main__":
    main()
