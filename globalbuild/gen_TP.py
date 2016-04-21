'''
Created on Aug 20, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
import numpy as np
from constants import *

G_args = (TP_OUT, BASINPOLY, TPPOLY)
G_kwargs = {'make_csv':"bin/%s.csv" % TP_OUT,
            'make_plot':"bin/%s.pdf" % TP_OUT,
            'make_map':"bin/%s.jpg" % TP_OUT,
            }

TEMP_TP_COPY = "in_memory/tp_tmp"
TEMP_AREA = "in_memory/tp_tmp2"
TEMP_INTERSECT = "in_memory/tp_tmp3"
TEMP_INTERSECT_AREA = "in_memory/tp_tmp4"

class gTP(generator.APGenerator):
    """gen(TP_OUT, BASINPOLY, TPPOLY, overwrite=True, workspace=WORKSPACE, make_csv=OUTCSV, make_plot=OUTPLOT)"""
    generator_name = "total phosprorous"
    plot_field_name = "TP"
    map_layer_label = "phosphorus yield"
    threshold_values = (0,10,20,40,80,999999999999)
    def __init__(self):
        super(gTP, self).__init__()

    def _make(self, output_file, basin_poly, tp_poly, **kwargs):
        print "calculating concentration"
        ap.CopyFeatures_management(tp_poly,TEMP_TP_COPY)
        
        print "calculating areas"
        ap.CalculateAreas_stats(basin_poly, TEMP_AREA)
        ap.AddField_management(TEMP_AREA, "base_area", "DOUBLE")
        ap.CalculateField_management(TEMP_AREA, "base_area", "!F_AREA!", "PYTHON")
        
        print "overlaying"
        ap.Identity_analysis(TEMP_AREA, TEMP_TP_COPY, TEMP_INTERSECT, "ALL", 0)
        
        print "calculating proportions"
        ap.CalculateAreas_stats(TEMP_INTERSECT, TEMP_INTERSECT_AREA)
        ap.AddField_management(TEMP_INTERSECT_AREA, "portion", "DOUBLE")
        ap.CalculateField_management(TEMP_INTERSECT_AREA, "portion", "0", "PYTHON")
        ap.CalculateField_management(TEMP_INTERSECT_AREA, "portion", "(!Yld_TP!>0)*!F_AREA!/!base_area!", "PYTHON")
        ap.AddField_management(TEMP_INTERSECT_AREA, "weighted_score", "DOUBLE")
        ap.CalculateField_management(TEMP_INTERSECT_AREA, "weighted_score", "!portion!*!Yld_TP!", "PYTHON")
        
        print "dissolving"
        ap.Dissolve_management(TEMP_INTERSECT_AREA,output_file,[BASIN_ID_FIELD],[["portion","SUM"],["weighted_score","SUM"]])
        ap.AddField_management(output_file, self.plot_field_name, "DOUBLE")
        ap.MakeFeatureLayer_management(output_file, "temp_layer") 
        ap.SelectLayerByAttribute_management("temp_layer", "NEW_SELECTION", '"SUM_portion" > 0')
        ap.CalculateField_management("temp_layer", self.plot_field_name, "!SUM_weighted_score!/!SUM_portion!", "PYTHON")
    
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,self.plot_field_name]
        array = super(gTP,self)._get_array(output_file, fields)
        return array

def gen(*args, **kwargs):
    return gTP().gen(*args, **kwargs)

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
    
