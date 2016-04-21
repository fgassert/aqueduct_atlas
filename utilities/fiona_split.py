#!/usr/bin/env python

import fiona
import os
import zipfile

folder = os.path.expanduser('~/tmp')
infile = os.path.expanduser('~/doc/GIS/shps/Aqueduct_river_basins.shp')
id_field = "BASIN_NAME"

def fiona_split(inshp,outdir,id_field):
    with fiona.drivers():
        with fiona.open(inshp,'r','ESRI Shapefile') as src:
            for f in src:
                o = os.path.splitext(os.path.basename(inshp))[0] + '_%s.shp' % f['properties'][id_field]
                
                with fiona.open(o,'w',
                                src.driver,
                                crs=src.crs,
                                schema=src.schema) as dst:
                    dst.write({'id':-1,
                               'geometry':f['geometry'],
                               'properties':f['properties']})
                with zipfile.ZipFile(os.path.join(outdir,o[:-4]+'.zip'),'w') as z:
                    for e in ['.shp','.shx','.dbf','.cpg','.prj']:
                        z.write(o[:-4]+e, arcname=os.path.basename(o[:-4]+e))
                        os.remove(o[:-4]+e)

  
if __name__ == "__main__":
    fiona_split(infile,folder,id_field)
