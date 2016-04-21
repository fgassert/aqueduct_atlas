'''
Created on Oct 15, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *
import matplotlib.mlab as mlab
import gen_merge

G_args=(BWS_OUT, BASINPOLY, BACSV, WITHDRAWALCSV, CONSUMPTIONCSV, AREACSV)
G_kwargs={'make_csv':"bin/%s.csv" % BWS_OUT, 
        'make_plot':"bin/%s.pdf" % BWS_OUT, 
        'make_map':"bin/%s.jpg" % BWS_OUT, 
        }

class gBWS(generator.APGenerator):
    """docstring for gBWS"""
    generator_name = "baseline water stress"
    plot_field_name = "BWS"
    threshold_values = (0,0.1,0.2,.4,.8,999999999999)
    map_layer_label = "withdrawal / renewable supply"
    c1 = .1
    base = 2
    category_names = MAP_CLASSES["BWS_cat"]
    
    def __init__(self):
        super(gBWS, self).__init__()
    
    def _make(self, output_file, basin_poly, ba_csv, withdrawal_csv, consumption_csv, area_csv, arid_thresh=0.03, use_thresh=0.012, **kwargs):
        print "loading data"
        ba = np.genfromtxt(ba_csv,np.double,skip_header=1,delimiter=',')
        area_arr = mlab.csv2rec(area_csv)
        ut_arr = mlab.csv2rec(withdrawal_csv)
        ct_arr = mlab.csv2rec(consumption_csv)
        
        ids = ba[:,0]
        
        mean_ba = np.mean(ba[:,1:],1)
        ut = gen_merge.arrange_vector_by_ids(ut_arr["ut"],ut_arr["basinid"],ids).astype(np.double)
        uc = gen_merge.arrange_vector_by_ids(ct_arr["ct"],ct_arr["basinid"],ids).astype(np.double)
        area = gen_merge.arrange_vector_by_ids(area_arr["f_area"],area_arr["basinid"],ids).astype(np.double)
        bws = ut/mean_ba
        
        miscmask = (ut/area<use_thresh)*(mean_ba/area<arid_thresh)
        #miscmask2 = (ut/area[:,1]<use_thresh)*(mean_ba/area[:,1]<arid_thresh)*(bws<.8)
        bws_s = self.score(bws)
        bws_s[miscmask] = MAXSCORE
        bws_cat = self.categorize(bws_s, miscmask)
        
        joinarray = np.rec.fromarrays((ba[:,0],mean_ba,ut,uc,bws,bws_s,bws_cat,area),names=(BASIN_ID_FIELD,"BA","WITHDRAWAL","CONSUMPTION",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name,"AREAM3"))
        
        print "joining data"
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,"WITHDRAWAL","CONSUMPTION","BA",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gBWS,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gBWS().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
