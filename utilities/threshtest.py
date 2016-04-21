'''
Created on Nov 15, 2012

@author: francis.gassert
'''

import gen_BWS as bws
import gen_WRI as wri
from constants import *

def main():
    bws.gen("BWS_thresh_012_03", BASINPOLY, BACSV, WITHDRAWALCSV, AREACSV, workspace=WORKSPACE, overwrite=True, use_thresh=0.012, arid_thresh=0.03, make_map="bin/BWS_thresh_012_03.mxd")
    bws.gen("BWS_thresh_01_01", BASINPOLY, BACSV, WITHDRAWALCSV, AREACSV, workspace=WORKSPACE, overwrite=True, use_thresh=0.01, arid_thresh=0.01)
    wri.gen("WRI_thresh_012_03", BASINPOLY, BACSV, FANCONSCSV, AREACSV, workspace=WORKSPACE, overwrite=True, use_thresh=0.012, arid_thresh=0.03)
    wri.gen("WRI_thresh_01_01", BASINPOLY, BACSV, FANCONSCSV, AREACSV, workspace=WORKSPACE, overwrite=True, use_thresh=0.01, arid_thresh=0.01)
    


if __name__ == '__main__':
    main()