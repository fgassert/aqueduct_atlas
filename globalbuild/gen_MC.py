'''
Created on Sept 7, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
import matplotlib.mlab as mlab
from constants import *

G_args=(MC_OUT, ADMINPOLY, MEDIACSV)
G_kwargs={'make_csv':"bin/%s.csv" % MC_OUT, 
        'make_plot':"bin/%s.pdf" % MC_OUT, 
        'make_map':"bin/%s.jpg" % MC_OUT, 
        }
FILTER_MIN_ARTICLES = 10000
MC_COUNTRY_ID = "iso_n3"

class gMC(generator.APGenerator):
    """docstring for gMC"""
    generator_name = "media coverage"
    plot_field_name = "MC"
    threshold_values = (0,0.0005,0.001,.002,.004,999999999999)
    map_layer_label = "Water issue articles / all articles"
    c1 = 0.0005
    base = 2
    category_names = MAP_CLASSES["MC_cat"]

    
    def __init__(self):
        super(gMC, self).__init__()
    
    def _make(self, output_file, admin_poly, media_csv, **kwargs):
        print "loading data"
        mc_arr = mlab.csv2rec(media_csv,delimiter=',')
        mc_arr=mc_arr[mc_arr[MC_COUNTRY_ID]!=0]
        id_field = mc_arr[MC_COUNTRY_ID]
        mc_water = mc_arr['mean_water'].astype(np.double)
        mc_all = mc_arr['mean_all'].astype(np.double)
        mc = mc_water/mc_all
        mc[(mc_all<FILTER_MIN_ARTICLES)]=None
        
        mc_s = self.score(mc)
        mc_cat = self.categorize(mc_s)
                
        joinarray = np.rec.fromarrays((id_field,mc_water,mc_all,mc,mc_s,mc_cat),names=(ADMIN_ID_FIELD,"MC_water","MC_all",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        print "joining data"
        ap.CopyFeatures_management(admin_poly,output_file)
        ap.da.ExtendTable(output_file,ADMIN_ID_FIELD,joinarray,ADMIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [ADMIN_ID_FIELD,"MC_water","MC_all",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gMC,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gMC().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
    #gMC().make_map("bin/%s_2.jpg" % MC_OUT, MC_OUT, map_values = (0,.0005,.001,.002,.004,999999999999))