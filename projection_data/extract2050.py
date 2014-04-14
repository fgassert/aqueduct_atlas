import pandas as pd
import math
import sys

mdls = [
    {
        'CCSM4':['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i5p1','r6i1p1'],
        'CNRM-CM5':['r1i1p1'],
        'GFDL-ESM2M':['r1i1p1'],
        'MPI-ESM-LR':['r1i1p1','r2i1p1','r3i1p1'],
        'MRI-CGCM3':['r1i1p1'],
        'inmcm4':['r1i1p1']
    },
    {
        'CCSM4':['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i5p1','r6i1p1'],
        'CNRM-CM5':['r1i1p1'],
        'GFDL-ESM2M':['r1i1p1'],
        'MPI-ESM-LR':['r1i1p1','r2i1p1','r3i1p1'],
        'MRI-CGCM3':['r1i1p1'],
        'inmcm4':['r1i1p1']
    },
    {
        'CCSM4':['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i5p1','r6i1p1'],
        'CNRM-CM5':['r1i1p1','r2i1p1','r4i1p1','r6i1p1'],
        'GFDL-ESM2M':['r1i1p1'],
        'MPI-ESM-LR':['r1i1p1','r2i1p1','r3i1p1'],
        'MRI-CGCM3':['r1i1p1'],
        'inmcm4':['r1i1p1']
    }]

rcps = ['historical','rcp45','rcp85']

def get_yr(pfx, ens, yr):
    df0 = pd.read_csv("%s_%s_%s_m.csv" % (pfx, ens[0], yr))
    for i in range(1,len(ens)):
        df0 += pd.read_csv("%s_%s_%s_m.csv" % (pfx, ens[i], yr))
    return df0/len(ens)

def main(fyear=2050, byear=1985, window=21):
    fyear = int(fyear)
    byear = int(byear)
    window = int(window)
    
    for r in range(len(rcps)):
        if r==0:
            tyear = byear
        else:
            tyear = fyear
        dfy0 = None
        for y in range(tyear-window//2,tyear+(window+1)//2):
            df0 = None
            for k,v in mdls[r].iteritems():
                pfx = "%s_%s" % (k,rcps[r])
                if df0 is None:
                    df0 = get_yr(pfx, v, y)
                else:
                    df0 += get_yr(pfx, v, y)
            df0 /= len(mdls[r])
            df0.to_csv('%s_%s.csv' % (rcps[r], y))
            print ('%s_%s.csv' % (rcps[r], y))
            if dfy0 is None:
                dfy0 = df0
            else:
                dfy0 += df0
        dfy0 /= 21
        dfy0.to_csv('21y_%s_%s.csv' % (rcps[r], tyear))
        print ('21y_%s_%s.csv' % (rcps[r], tyear))
        
    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
    else:
        main()
