

import spatial_weighted_stats as sw

working_directory = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/"
scratch_gdb = "scratch.gdb"

# Original polygon data
input_polys = "global_BWS_20140121"
# Attribute fields to aggregate (must be numeric)        
input_fields = ["CTA"]
# input_fields = [""]

# Weights for aggregation
weight_rasters = ["cellarea_ha"]

# Polygons to aggregate data into
output_polys = ["WULCA/BWF.shp"]

# Csv to save statistics in
out_file = "amb_01"

# Resolution to which weight rasters should be resampled before aggregation in decimal degrees,
#  <None> to keep original resolution
downsample = None # 1.0/24 # in dd

# No data value
null_value = -32767

# Statistics to calculate
stats = {"mean":1,"v":0,"sd":1,"mode":0,"hist":0,"min":0,"max":0,"sum":0,"nan":1,"hist":0}

sw.spatial_weighted_stats(working_directory, scratch_gdb, input_polys, input_fields,
                    weight_rasters, out_file, output_polys,
                    stats, downsample, null_value)