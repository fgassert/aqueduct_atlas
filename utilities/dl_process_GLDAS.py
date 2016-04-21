'''
Created on Aug 28, 2013

@author: francis.gassert
'''

import os
import urllib2
from multiprocessing import Pool

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"

def worker(x):
    try:
        out = "%stmp/%s.grb" % (CWD, x)
        if not os.path.exists(out):
            u = "ftp://hydro1.sci.gsfc.nasa.gov/data/s4pa/GLDAS/GLDAS_NOAH10_M.020/%s/GLDAS_NOAH10_M.A%s.020.grb" % (x[:4],x)
            r=urllib2.urlopen(u)
            f=open(out,'wb')
            f.write(r.read())
            f.close()
    except Exception as e:
        print e

def main():
    
    ulist = []
    for y in range(1950,2011):
        for m in range(1,13):
            x = "{0:04d}{1:02d}".format(y,m)
            ulist.append(x)
    
    p = Pool(processes=4)
    result = p.map(worker, ulist)
    print result
    print "complete"


if __name__ == '__main__':
    main()
