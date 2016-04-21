'''
Created on Aug 28, 2013

@author: francis.gassert
'''

# import arcpy as ap
import os
import urllib2
from multiprocessing import Pool

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"

def worker(x):
    try:
        out = "%stmp/%s.asc.zip" % (CWD, x)
        if not os.path.exists(out):
            u = "http://www.geog.mcgill.ca/landuse/pub/Data/175crops2000/ArcASCII-Zip/%s.asc.zip" % (x)
            r=urllib2.urlopen(u)
            f=open(out,'wb')
            f.write(r.read())
            f.close()
    except Exception as e:
        print e

def main():
    
    clist = [
        "coffee",
        "cocoa",
        "sugarcane",
        "orange",
        "maize",
        "maizefor",
        "wheat",
        "soybean",
        "cotton",
        "oats",
        "rice",
        "oilpalm",
        "rapeseed",
        "rubber",
        "11CropGroups/G_Cereals",
        "11CropGroups/G_Fiber",
        "11CropGroups/G_Forage",
        "11CropGroups/G_Fruit",
        "11CropGroups/G_Oilcrops",
        "11CropGroups/G_Pulses",
        "11CropGroups/G_Roots&Tubers",
        "11CropGroups/G_SugarCrops",
        "11CropGroups/G_Treenuts"]
    ulist = []
    for c in clist:
        ulist.append("%s_harea"% c)

    p = Pool(processes=4)
    result = p.map(worker, ulist)
    print result
    print "complete"


if __name__ == '__main__':
    main()
