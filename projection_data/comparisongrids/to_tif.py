
import pandas as pd
import netCDF4 as nc
import rasterio
from rasterio import Affine as A

innc = ["2010_waterdemand_30min_irrigation.nc",
        "2010_waterdemand_30min_total.nc"]
outras = ["2010_irr.tif",
          "2010_tot.tif"]
varname = ['incr',
           'totd']

def main():
    
    for i in range(2):
        dat = nc.Dataset(innc[i])
        print dat
        
        #sum monthly values for 2010
        dat2010 = dat.variables[varname[i]][600:611,:,:].sum(0)
        cols = 720
        rows = 360
        d = 1/2.0
    
        with rasterio.open(outras[i],'w',
                       'GTiff',
                       width=cols,
                       height=rows,
                       dtype=dat2010.dtype,
                       crs={'init': 'EPSG:4326'},
                       transform=A.translation(-cols*d/2, rows*d/2) * A.scale(d, -d),
                       count=1) as dst:
            dst.write_band(1,dat2010)




if __name__ == "__main__":
    main()
