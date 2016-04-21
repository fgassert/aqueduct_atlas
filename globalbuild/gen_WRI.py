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

G_args=(WRI_OUT, BASINPOLY, BACSV, FANCONSCSV, AREACSV)
G_kwargs={'make_csv':"bin/%s.csv" % WRI_OUT, 
        'make_plot':"bin/%s.pdf" % WRI_OUT, 
        'make_map':"bin/%s.jpg" % WRI_OUT, 
        }

class gWRI(generator.APGenerator):
    """docstring for gWRI"""
    generator_name = "Return flow ratio"
    plot_field_name = "WRI"
    threshold_values = (0,0.1,0.2,.4,.8,999999999999)
    map_layer_label = "upstream non-consumptive use / renewable supply"
    c1 = .1
    base = 2
    category_names = MAP_CLASSES["WRI_cat"]

    def __init__(self):
        super(gWRI, self).__init__()
    
    def _make(self, output_file, basin_poly, ba_csv, fa_ncons_csv, area_csv, arid_thresh=0.03, use_thresh=0.012, **kwargs):
        print "loading data"
        ba = np.genfromtxt(ba_csv,np.double,skip_header=1,delimiter=',')
        area_arr = mlab.csv2rec(area_csv)
        nc_arr = mlab.csv2rec(fa_ncons_csv)
        
        ids = ba[:,0]
        
        mean_ba = np.mean(ba[:,1:],1)
        ncons = gen_merge.arrange_vector_by_ids(nc_arr["ncons"],nc_arr["basinid"],ids).astype(np.double)
        area = gen_merge.arrange_vector_by_ids(area_arr["f_area"],area_arr["basinid"],ids).astype(np.double)
        
        wri = ncons/mean_ba
        
        miscmask = (ncons/area<use_thresh)*(mean_ba/area<arid_thresh)
        wri_s = self.score(wri)
        wri_s[miscmask] = MINSCORE
        wri_cat = self.categorize(wri_s, miscmask)
        
        
        joinarray = np.rec.fromarrays((ba[:,0],mean_ba,ncons,wri,wri_s,wri_cat),names=(BASIN_ID_FIELD,"BA","FA_NCONS",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        print "joining data"
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,"BA","FA_NCONS",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gWRI,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gWRI().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)