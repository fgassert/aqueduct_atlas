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

G_args = (ECO_V_OUT, BASINPOLY, AMPHIBPOLY)
G_kwargs = {'make_csv':"bin/%s.csv" % ECO_V_OUT,
            'make_plot':"bin/%s.pdf" % ECO_V_OUT,
            'make_map':"bin/%s.jpg" % ECO_V_OUT,
            }

MIN_COUNT = 2

class gECO_V(generator.APGenerator):
    """gen(ECO_V_OUT, BASINPOLY, AMPHIBPOLY, overwrite=True, workspace=WORKSPACE, make_csv=OUTCSV, make_plot=OUTPLOT)"""
    generator_name = "threatened amphibians"
    plot_field_name = "ECO_V"
    threshold_values = (0,0,.05,.15,.35,999999999999)
    map_layer_label = "Percent threatened freshwater amphibians"
    c1 = .05
    base = 2
    category_names = MAP_CLASSES["ECO_V_cat"]

    def __init__(self):
        super(gECO_V, self).__init__()

    def _make(self, output_file, basin_poly, amphib_poly, **kwargs):
        print "joining amphibs"
        fm = ap.FieldMappings()
        fm.addTable(basin_poly)
        tempfm = ap.FieldMappings()
        tempfm.addTable(amphib_poly)
        for field in ["THREAT","EX","EW","EN","VU","CR"]:
            findex = tempfm.findFieldMapIndex(field)
            tempmap = tempfm.getFieldMap(findex)
            tempmap.mergeRule = "Sum"
            fm.addFieldMap(tempmap)
        ap.SpatialJoin_analysis(basin_poly, amphib_poly, output_file, "JOIN_ONE_TO_ONE", "KEEP_ALL", fm, "intersect")
        
        print "calculating percent threatened"
        #extract fields from feature class
        fields = (BASIN_ID_FIELD,"join_count","THREAT","EX","EW")
        arr = ap.da.FeatureClassToNumPyArray(output_file, fields, null_value=0)
        
        #calculate new fields
        total = arr["join_count"].astype(np.double)
        threat_ex = arr["THREAT"]
        threat_ex = threat_ex.astype(np.double)
        eco_v = threat_ex / (total-arr["EX"]-arr["EW"])
        eco_v[total<MIN_COUNT]=None
        
        eco_v_s = self.score(eco_v+0.05)
        eco_v_cat = self.categorize(eco_v_s)
        
        joinarray = np.rec.fromarrays((arr[BASIN_ID_FIELD],threat_ex,total,eco_v,eco_v_s,eco_v_cat),names=(BASIN_ID_FIELD,"THREAT_EX","ALL_AMPH",self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        #rejoin to feature class
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
    
    def _get_array(self, output_file):
        print "generating table"
        fields = (BASIN_ID_FIELD, "ALL_AMPH", "THREAT_EX", self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name)
        array = super(gECO_V,self)._get_array(output_file, fields)
        return array

def gen(*args, **kwargs):
    return gECO_V().gen(*args, **kwargs)

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
    #output_file = "CRB_ECOV_20121210"
    #basin_poly = r"M:\Working\Aqueduct\Colorado River Basin (CRB)\Basin Boundaries\CRB_WGS84-20120221.shp"
    #amphib_poly = AMPHIBPOLY
    #kwargs = {'make_csv':"bin/%s.csv" % output_file,
    #        'make_plot':"bin/%s.pdf" % output_file,
    #        'make_map':"bin/%s.jpg" % output_file,
    #        }
    #gen(output_file, basin_poly, amphib_poly, workspace=WORKSPACE, overwrite=True, **kwargs)
