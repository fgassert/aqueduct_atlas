'''
Created on Sept 7, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *

G_args=(STOR_OUT, BASINPOLY, BTCSV, STORAGECSV)
G_kwargs={'make_csv':"bin/%s.csv" % STOR_OUT, 
        'make_plot':"bin/%s.pdf" % STOR_OUT, 
        'make_map':"bin/%s.jpg" % STOR_OUT, 
        }

ZERO_STORAGE=None

class gSTOR(generator.APGenerator):
    """docstring for gSTOR"""
    generator_name = "upstream storage"
    plot_field_name = "STOR"
    threshold_values = (999999999999,1,.5,.25,.125,0)
    map_layer_label = "upstream storage / mean discharge"
    c1 = 1
    base = 2
    category_names = MAP_CLASSES["STOR_cat"]

    def __init__(self):
        super(gSTOR, self).__init__()
    
    def _make(self, output_file, basin_poly, bt_csv, storage_csv,**kwargs):
        print "loading data"
        bt = np.genfromtxt(bt_csv,np.double,skip_header=1,delimiter=',')
        stor_arr = np.genfromtxt(storage_csv,np.double,skip_header=1,delimiter=',')
        if any(bt[:,0]!=stor_arr[:,0]):
            raise Exception("ID colums do not match")
        mean_bt = np.mean(bt[:,1:],1)
        FA_stor = stor_arr[:,2]*1000000
        mean_bt[(mean_bt==0)] = 1
        stor = FA_stor/mean_bt
        stor[(FA_stor==0)] = ZERO_STORAGE
        
        stor_s = self.score(stor,invert=True)
        stor_cat = self.categorize(stor_s)
        
        joinarray = np.rec.fromarrays((bt[:,0],mean_bt,FA_stor,stor,stor_s,stor_cat),names=(BASIN_ID_FIELD,"BT","FA_STOR",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        print "joining data"
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,"BT","FA_STOR",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gSTOR,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gSTOR().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)