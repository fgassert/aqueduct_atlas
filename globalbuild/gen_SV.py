'''
Created on Sept 11, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *

G_args = (SV_OUT, BASINPOLY, BTMONTHLYCSV)
G_kwargs = {'make_csv':"bin/%s.csv" % SV_OUT,
            'make_plot':"bin/%s.pdf" % SV_OUT,
            'make_map':"bin/%s.jpg" % SV_OUT,
            }

class gSV(generator.APGenerator):
    """docstring for gSV"""
    generator_name = "seasonal variability"
    plot_field_name = "SV"
    threshold_values = (0,.33,.67,.1,1.33,999999999999)
    map_layer_label = "Stdev. of discharge / mean monthly discharge"
    c1 = 1.0/3
    base = 1.0/3
    category_names = MAP_CLASSES["SV_cat"]
    
    def __init__(self):
        super(gSV, self).__init__()
    
    def _make(self, output_file, basin_poly, bt_monthly, **kwargs):
        print "loading data"
        bt = np.genfromtxt(bt_monthly,np.double,skip_header=1,delimiter=',')
        monthly_means = np.ndarray((bt.shape[0],12), dtype=np.double)
        for i in range(12):
            idx = np.arange(1+i,bt.shape[1]-1,12)
            monthly_means[:,i]=np.mean(bt[:,idx],1)
        mean_bt = np.mean(monthly_means,1)
        std_bt = np.std(monthly_means,1,ddof=1)
        sv = std_bt/mean_bt
        
        sv_s = self.score(sv, logscale=False)
        sv_cat = self.categorize(sv_s)
        
        joinarray = np.rec.fromarrays((bt[:,0],mean_bt,std_bt,sv,sv_s,sv_cat),names=(BASIN_ID_FIELD,"MEANMONTHYBT","STDMONTLYBT",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        print "joining data"
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,"MEANMONTHYBT","STDMONTLYBT",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gSV,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gSV().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
    #gen(*G_args, workspace=WORKSPACE, overwrite=False, map_values = (0,.5,1,1.5,2,99999), **G_kwargs)