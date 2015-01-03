#!/bin/bash

gdalwarp 2010_irr.tif 2010_irr_5min.tif -tr .08333333333 .0833333333
gdalwarp 2010_tot.tif 2010_tot_5min.tif -tr .08333333333 .0833333333
