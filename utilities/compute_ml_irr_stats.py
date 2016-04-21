

import spatial_weighted_stats as sw
import os

working_directory = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/marginal_lands"
os.chdir(working_directory)

# Original polygon data

input_polys = "marginal_land_inputs.gdb/projections_20140303"
#input_polys = "marginal_land_inputs.gdb/global_master_20130123"
# Attribute fields to aggregate (must be numeric)        

#input_fields = ["GW_s"]

input_fields = ["WWR_ch_2030_RCP45_SSP2","WWR_ch_2030_RCP85_SSP2","WWR_ch_2040_RCP45_SSP2","WWR_ch_2040_RCP85_SSP2"]
# input_fields = [""]
# Weights for aggregation
weight_rasters = "marginal_land_inputs.gdb/aai_ha"

# Polygons to aggregate data into
output_polys = "marginal_land_inputs.gdb/mena_plus"

# Csv to save statistics in
out_file = "aai_stress"

# Resolution to which weight rasters should be resampled before aggregation in decimal degrees,
#  <None> to keep original resolution
downsample = None # 1.0/24 # in dd

# No data value
null_value = -32767

# Statistics to calculate
stats = {"mean":0,"v":0,"sd":0,"mode":0,"hist":0,"min":0,"max":0,"sum":0,"nan":0,"hist":[0,.5,2**-.5,1,2**.5,2,100]}
#stats = {"mean":1,"v":0,"sd":0,"mode":0,"hist":0,"min":0,"max":0,"sum":1,"nan":1,"hist":[0,1,2,3,4,5,100]}

sw.spatial_weighted_stats(input_polys, input_fields,
                    weight_rasters, out_file, output_polys,
                    stats, downsample, null_value)