
import pandas as pd
import numpy as np
import sys, os
import fiona_join

SHP = "shps/Basins_15006-20130820.shp"
OUTSHP = "shps/projection_data_20140416.shp"
DUMPCSV = "prepped.csv"
INDIR = "csvs"

BA = "Summary-20140630.csv"
BTm = ["bt_mean_rcp45.csv","bt_mean_rcp85.csv"]
BTcv = ["bt_cv_rcp45.csv","bt_cv_rcp85.csv"]
SVm = ["sv_mean_rcp45.csv","sv_mean_rcp85.csv"]
SVcv = ["sv_cv_rcp45.csv","sv_cv_rcp85.csv"]
AVm = ["iav_mean_rcp45.csv","iav_mean_rcp85.csv"]
AVcv = ["iav_cv_rcp45.csv","iav_cv_rcp85.csv"]
AREA = "basin_area_20140121.csv"
AREAM2 = "F_AREA"
LABELS = "labels_20140416.csv"

csvSS = ['RCP45_SSP2','RCP85_SSP2','RCP85_SSP3']

II = ['ws','ut','bt','sv']#,'av']
YY = ['20','30','40']
SS = ['24','28','38']
R = ['t','c','u']

csvYY = ['2020','2030','2040']
BASEYEAR = '2010'

LARGE_NUMBER = 1e16
NROWS = 15006
BASINID = "BasinID"
NODATA = "-32767"
CHANGECATEGORIES=7


__csvs = {}
def DF(fname):
    """loads named csv into dataframe"""
    if fname not in __csvs:
        df = pd.read_csv(os.path.join(INDIR,fname))
        if BASINID in df.columns:
            df.sort(BASINID,inplace=True)
            df.reset_index()
        if len(df) != NROWS: print "warning: incorrect csv length: %s, %s" % (fname,len(df))
        __csvs[fname] = df
    return __csvs[fname]


def wstcalc(s,y):
    raw = DF(BA)["WWR_%s_%s" % (csvYY[y],csvSS[s])]
    t = get_log_thresholds(5,2,.1)
    score = threshold_score(raw,t)
    mask = ((DF(BA)["Ut_%s_%s" % (csvYY[y],csvSS[s])]/DF(AREA)[AREAM2] < 0.012) & 
            (DF(BA)["Ba_%s_%s" % (csvYY[y],csvSS[s])]/DF(AREA)[AREAM2] < 0.03))
    score[score==5] = 6
    score[np.isnan(np.asarray(raw))] = 6
    score[np.asarray(mask)] = 5
    labels = DF(LABELS)['wst'][score]
    return raw,labels
def wsccalc(s,y):
    raw = DF(BA)["WWR_ch_%s_%s" % (csvYY[y],csvSS[s])]
    t = get_change_thresholds(CHANGECATEGORIES,2,rate=.5)
    score = threshold_score(raw,t)
    mask = (((DF(BA)["WWR_%s_%s" % (csvYY[y],csvSS[s])] <= .1) &
             (raw > 0)) |
            ((DF(BA)["WWR_%s_%s" % (csvYY[y],csvSS[s])] > .8) &
             (raw < 0)))
    score[np.asarray(mask)] = CHANGECATEGORIES//2
    score[np.isnan(np.asarray(raw))] = CHANGECATEGORIES
    labels = DF(LABELS)['wsc'][score]
    return raw,labels
def wsucalc(s,y):
    raw = np.zeros(NROWS,dtype=int)
    labels = np.array(["N/A"])[raw]
    return raw,labels

def uttcalc(s,y):
    raw = DF(BA)["Ut_%s_%s" % (csvYY[y],csvSS[s])]/DF(AREA)[AREAM2]
    t = get_log_thresholds(5,np.sqrt(10),.01)
    score = threshold_score(raw, t)
    labels = DF(LABELS)['utt'][score]    
    return raw,labels
def utccalc(s,y):
    raw = DF(BA)["Ut_ch_%s_%s" % (csvYY[y],csvSS[s])]
    t = get_change_thresholds(CHANGECATEGORIES,rate=.25)
    score = threshold_score(raw, t)
    score[np.isnan(np.asarray(raw))] = CHANGECATEGORIES
    labels = DF(LABELS)['utc'][score]
    return raw,labels
def utucalc(s,y):
    raw = np.zeros(NROWS,dtype=int)
    labels = np.array(["N/A"])[raw]
    return raw,labels

def bttcalc(s,y):
    raw = DF(BTm[s])[csvYY[y]]/DF(AREA)[AREAM2]
    t = get_log_thresholds(8,np.sqrt(10),.01)
    score = threshold_score(raw, t)
    labels = DF(LABELS)['btt'][score]    
    return raw,labels
def btccalc(s,y):
    raw = (DF(BTm[s])[csvYY[y]] / 
           DF(BTm[s])[BASEYEAR])
    t = get_change_thresholds(CHANGECATEGORIES,rate=.25)
    score = threshold_score(raw, t)
    score[np.isnan(np.asarray(raw))] = CHANGECATEGORIES
    labels = DF(LABELS)['btc'][score]
    return raw,labels
def btucalc(s,y):
    raw = (DF(BTcv[s])[csvYY[y]])
    t = get_mask_thresholds(rate=.25)
    score = threshold_score(raw, t)
    labels = DF(LABELS)['btu'][score]
    return raw,labels

def svtcalc(s,y):
    raw = DF(SVm[s])[csvYY[y]]
    t = get_linear_thresholds(5,.33,.33)
    score = threshold_score(raw, t)
    score[np.asarray(raw==0)] = 5
    labels = DF(LABELS)['svt'][score]    
    return raw,labels
def svccalc(s,y):
    raw = (DF(SVm[s])[csvYY[y]] / 
           DF(SVm[s])[BASEYEAR])
    t = get_change_thresholds(CHANGECATEGORIES, rate=.125)
    score = threshold_score(raw, t)
    score[np.isnan(np.asarray(raw))] = CHANGECATEGORIES
    labels = DF(LABELS)['svc'][score]
    return raw,labels
def svucalc(s,y):
    raw = (DF(SVcv[s])[csvYY[y]])
    t = get_mask_thresholds(rate=.125)
    score = threshold_score(raw, t)
    labels = DF(LABELS)['svu'][score]
    return raw,labels

def avtcalc(s,y):
    raw = DF(AVm[s])[csvYY[y]]
    t = get_linear_thresholds(5,.25,.25)
    score = threshold_score(raw, t)
    score[np.asarray(raw==0)] = 5
    labels = DF(LABELS)['avt'][score]    
    return raw,labels
def avccalc(s,y):
    raw = (DF(AVm[s])[csvYY[y]] / 
           DF(AVm[s])[BASEYEAR])
    t = get_change_thresholds(CHANGECATEGORIES, rate=.125)
    score = threshold_score(raw, t)
    score[np.isnan(np.asarray(raw))] = CHANGECATEGORIES
    labels = DF(LABELS)['avc'][score]
    return raw,labels
def avucalc(s,y):
    raw = (DF(AVcv[s])[csvYY[y]])
    t = get_mask_thresholds(rate=.125)
    score = threshold_score(raw, t)
    labels = DF(LABELS)['avu'][score]
    return raw,labels



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
    return np.sum(vec.as_matrix() > thresholds[:,np.newaxis],0)



def prep_data():
    """"""

    outdf = pd.DataFrame()
    outdf[BASINID] = np.arange(NROWS)+1
    datalbls = []

    generators = [
        [wstcalc,wsccalc,wsucalc],
        [uttcalc,utccalc,utucalc],
        [bttcalc,btccalc,btucalc],
        [svtcalc,svccalc,svucalc],
        [avtcalc,avccalc,avucalc],
    ]

    for i in range(len(II)):
        for r in range(len(R)):
            for s in range(len(SS)):
                for y in range(len(YY)):
                    ss = s
                    if i>1 and s>1: ss=1 #no ssps for supply indicators
                    raw,labels = generators[i][r](ss,y)
                    outlblr = "%s%s%s%sr" % (II[i],YY[y],SS[s],R[r])
                    outlbll = "%s%s%s%sl" % (II[i],YY[y],SS[s],R[r])

                    datalbls.append(outlbll)
                    outdf[outlblr] = np.asarray(raw)
                    outdf[outlbll] = np.asarray(labels)
            
    return outdf
    

def main():
    arr = prep_data()
    print "saving csv"
    arr.fillna(NODATA, inplace=True)
    arr.to_csv(DUMPCSV)
    print 'joining'
    fiona_join.joincsvtoshp(SHP,BASINID,DUMPCSV,BASINID,OUTSHP)
    print 'complete'
    
if __name__ == '__main__':
    main()
