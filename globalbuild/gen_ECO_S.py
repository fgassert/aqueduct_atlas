'''
Created on Sept 6, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *

G_args = (ECO_S_OUT, BASINPOLY, BTCSV, PROTCSV)
G_kwargs = {'make_csv':"bin/%s.csv" % ECO_S_OUT,
            'make_plot':"bin/%s.pdf" % ECO_S_OUT,
            'make_map':"bin/%s.jpg" % ECO_S_OUT,
            }

class gECO_S(generator.APGenerator):
    """docstring for gECO_S"""
    generator_name = "protected land"
    plot_field_name = "ECO_S"
    threshold_values = (999999999999,.4,.2,.1,.05,0)
    map_layer_label = "Discharge from protected land / mean discharge"
    c1 = .4
    base = 2
    category_names = MAP_CLASSES["ECO_S_cat"]

    def __init__(self):
        super(gECO_S, self).__init__()
    
    def _make(self, output_file, basin_poly, bt_csv, prot_csv, **kwargs):
        print "loading data"
        bt = np.genfromtxt(bt_csv,np.double,skip_header=1,delimiter=',')
        prot = np.genfromtxt(prot_csv,np.double,skip_header=1,delimiter=',')
        if any(bt[:,0]!=prot[:,0]):
            raise Exception("ID colums do not match")
        mean_bt = np.mean(bt[:,1:],1)    
        mean_prot = np.mean(prot[:,1:],1)
        eco_s = mean_prot/mean_bt
        
        eco_s_s = self.score(eco_s,invert=True)
        eco_s_cat = self.categorize(eco_s_s)
        
        joinarray = np.rec.fromarrays((bt[:,0],mean_bt,mean_prot,eco_s,eco_s_s,eco_s_cat),names=(BASIN_ID_FIELD,"MEANBT","PROT",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        print "joining data"
        ap.CopyFeatures_management(basin_poly,output_file)
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,"MEANBT","PROT",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gECO_S,self)._get_array(output_file, fields)
        return array
        
       
def gen(*args, **kwargs):
    return gECO_S().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=False, **G_kwargs)