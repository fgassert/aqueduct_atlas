

import spatial_weighted_stats as sw

working_directory = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
scratch_gdb = "scratch.gdb"

# Original polygon data
input_polys = "global_maps/aqueduct_global_dl_20130123.gdb/global_master_20130123"
# input_polys = "../BasinDownloads20130127/TCCC_Water_Risk.gdb/TCCC_Water_Risk_WM"
# Attribute fields to aggregate (must be numeric)        
input_fields = ["BWS_s"]
# input_fields = [""]

# Weights for aggregation
weight_rasters = ["crops_m3.gdb/maize_yh"]

# Polygons to aggregate data into
output_polys = ["latam"]

# Csv to save statistics in
out_file = "latam_01"

# Resolution to which weight rasters should be resampled before aggregation in decimal degrees,
#  <None> to keep original resolution
downsample = None # 1.0/24 # in dd

# No data value
null_value = -32767

# Statistics to calculate
stats = {"mean":1,"v":0,"sd":0,"mode":0,"hist":0,"min":0,"max":0,"sum":1,"nan":1,"hist":[0,1,2,3,4,5]}

sw.spatial_weighted_stats(working_directory, scratch_gdb, input_polys, input_fields,
                    weight_rasters, out_file, output_polys,
                    stats, downsample, null_value)