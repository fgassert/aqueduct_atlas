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

G_args=(DRO_OUT, BASINPOLY, DROUGHTRASTER2)
G_kwargs={'make_csv':"bin/%s.csv" % DRO_OUT, 
        'make_plot':"bin/%s.pdf" % DRO_OUT, 
        'make_map':"bin/%s.jpg" % DRO_OUT, 
        }

TEMP_DOWNSCALE = "DRO_tmp"
TEMP_TABLE = "in_memory/DRO_tmp2"
DOWNSCALE_RESOLUTION = ".01"

class gDRO(generator.APGenerator):
    """docstring for gDRO"""
    generator_name = "droughts"
    plot_field_name = "DRO"
    threshold_values = (0,20,30,40,50,999999999999)
    map_layer_label = "drought severity"
    c1 = 20
    base = 10
    category_names = MAP_CLASSES["DRO_cat"]

    def __init__(self):
        super(gDRO, self).__init__()
    
    def _make(self, output_file, basin_poly, drought_raster, **kwargs):
        print "resampling"
        ap.Resample_management(drought_raster,TEMP_DOWNSCALE,DOWNSCALE_RESOLUTION,"NEAREST")
        print "calculating zones"
        ap.CheckOutExtension("Spatial")
        ap.sa.ZonalStatisticsAsTable(basin_poly,BASIN_ID_FIELD,TEMP_DOWNSCALE,TEMP_TABLE,"DATA","MEAN")
        ap.CheckInExtension("Spatial")
        ap.CopyFeatures_management(basin_poly,output_file)
        print "joining"
        arr = ap.da.TableToNumPyArray(TEMP_TABLE,(BASIN_ID_FIELD,"MEAN"))
        oid = arr[BASIN_ID_FIELD]
        dro = arr["MEAN"]
        
        dro_s = self.score(dro, False)
        dro_cat = self.categorize(dro_s)
        
        joinarray = np.rec.fromarrays((oid,dro,dro_s,dro_cat),names=(BASIN_ID_FIELD,self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name))
        
        ap.da.ExtendTable(output_file,BASIN_ID_FIELD,joinarray,BASIN_ID_FIELD)
        
    def _get_array(self, output_file):
        print "generating table"
        fields = [BASIN_ID_FIELD,self.plot_field_name,"%s_s" % self.plot_field_name,"%s_cat" % self.plot_field_name]
        array = super(gDRO,self)._get_array(output_file, fields)
        return array
       
def gen(*args, **kwargs):
    return gDRO().gen(*args, **kwargs) 

if __name__ == '__main__':
    gen(*G_args, workspace=WORKSPACE, overwrite=True, **G_kwargs)
    #output_file = "CRB_DRO_20121217"
    #basin_poly = r"M:\Working\Aqueduct\Colorado River Basin (CRB)\Basin Boundaries\CRB_WGS84-20120221.shp"
    #drought_raster = DROUGHTRASTER2
    #kwargs = {'make_csv':"bin/%s.csv" % output_file,
    #        'make_plot':"bin/%s.pdf" % output_file,
    #        'make_map':"bin/%s.jpg" % output_file,
    #        }
    #gen(output_file, basin_poly, drought_raster, workspace=WORKSPACE, overwrite=True, **kwargs)