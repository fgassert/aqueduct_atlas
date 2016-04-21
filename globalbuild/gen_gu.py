'''
Created on Aug 20, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import generator
from constants import *

G_args = (GU_OUT, BASINPOLY, ADMINPOLY, GWPOLY, LAKEPOLY, ADD_FEATURES)
G_kwargs = {'make_csv':"bin/%s.csv" % GU_OUT,
            'tolerance':GU_TOLERANCE,
            'dice':GU_DICE
            }

TMP_GU = "tmpGU"
TMP_GU2 = "tmpGU2"
TMP_SIMP = "tmpGUSIMP"
TMP_REP = "tmpGUSIMPrep"

COUNTRY_ORIG_NAME = "GEOUNIT"
ADMIN_ORIG_ID = "CountryID"
REQ_FIELDS = (GU_FIELD, BASIN_ID_FIELD, ADMIN_ID_FIELD, GW_ID_FIELD, COUNTRY_FIELD, BASIN_NAME_FIELD)

class gGU(generator.APGenerator):
    """docstring for gGU"""
    generator_name = "GU"
    plot_field_name = "GU"
    def __init__(self):
        super(gGU, self).__init__()
    
    def _make(self, output_file, basin_poly, admin_poly, gw_poly, lake_poly, add_features, tolerance = "0", dice=False, **kwargs):
        #print "simplifying"
        #ap.SimplifyPolygon_cartography(basin_poly,TMP_SIMP,"BEND_SIMPLIFY","2 kilometers",None,"RESOLVE_ERRORS")
        #ap.RepairGeometry_management(TMP_SIMP,TMP_REP)
        print "intersecting"        
        if dice:
            ap.MakeFeatureLayer_management(admin_poly,"admin_layer")
            oid_name = ap.Describe(admin_poly).OIDFieldName
            ids = ap.da.FeatureClassToNumPyArray(admin_poly,oid_name)
            gu_name_list = []
            fm = ap.FieldMappings()
            for i in ids[oid_name]:
                print "intersecting country %s of %s" % (i, len(ids[oid_name]))
                ap.SelectLayerByAttribute_management("admin_layer", None,'"%s" = %s' % (oid_name, i))
                gu_name = TMP_GU+str(i)
                ap.Intersect_analysis([basin_poly,"admin_layer"],gu_name)
                gu_name_list.append(gu_name)
                fm.addTable(gu_name)
            
            print "merging"
            ap.Merge_management(gu_name_list,TMP_GU,fm)
        else:
            ap.Intersect_analysis([basin_poly, admin_poly], TMP_GU, cluster_tolerance = tolerance)
        
        print "adding aquifers"
        ap.Identity_analysis(TMP_GU, gw_poly, TMP_GU2)
        ap.Erase_analysis(TMP_GU2, lake_poly, output_file)
        print "adding extra features"
        ap.Append_management(add_features, output_file, "NO_TEST")
        
        ap.AddField_management(output_file, GU_FIELD, "LONG")
        if COUNTRY_ORIG_NAME != COUNTRY_FIELD:
            ap.AddField_management(output_file, COUNTRY_FIELD, "TEXT")
            ap.CalculateField_management(output_file, COUNTRY_FIELD, "!%s!" % COUNTRY_ORIG_NAME, "PYTHON")
        if ADMIN_ORIG_ID != ADMIN_ID_FIELD:
            ap.AddField_management(output_file, ADMIN_ID_FIELD, "DOUBLE")
            ap.CalculateField_management(output_file, ADMIN_ID_FIELD, "!%s!" % ADMIN_ORIG_ID, "PYTHON")
        describe = ap.Describe(output_file)
        OID = describe.OIDFieldName
        ap.CalculateField_management(output_file, GU_FIELD, "!%s!" % OID, "PYTHON")
        
        drop = [f.baseName for f in ap.ListFields(output_file) if not(f.required) and f.baseName not in REQ_FIELDS]
        if len(drop)>0:
            ap.DeleteField_management(output_file,drop)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = REQ_FIELDS
        array = super(gGU,self)._get_array(output_file, fields, null_value=-1)
        array[BASIN_NAME_FIELD][array[BASIN_NAME_FIELD]=='-1']=""
        return array
       
def gen(*args, **kwargs):
    return gGU().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace = WORKSPACE, overwrite = True, **G_kwargs)