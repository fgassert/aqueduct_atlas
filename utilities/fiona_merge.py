
import fiona
import os
import zipfile
import sys
sys.settrace

WORKING_DIRECTORY = "watersheds/"
OUT_SHP = "out.shp"

def main(d, out):
    fs = os.listdir(d)
    schema = None
    
    # peek schema
    for f in fs:
        ext = os.path.splitext(f)[1]
        if ext == ".zip":
            with zipfile.ZipFile(os.path.join(d,f)) as z:
                shps = [s for s in z.namelist()
                        if os.path.splitext(s)[1] == '.shp']
            if len(shps):
                with fiona.open("/"+shps[0],
                                vfs="zip://"+os.path.join(d,f)
                ) as src:
                    schema = src.schema
                    crs = src.crs
                break
        elif ext == ".shp":
            print f
            with fiona.open(os.path.join(d,f)) as src:
                schema = src.schema
                crs = src.crs
            break
    if schema == None:
        print "ERROR: failed to peek schema"
        return
    schema['properties']['fname'] = 'str'
    with fiona.drivers():
        with fiona.open(os.path.join(d,out),'w',
                        crs=crs,
                        driver="ESRI Shapefile",
                        schema=schema
        ) as dst:
            for f in fs:
                base,ext = os.path.splitext(f)
                if ext == ".zip":
                    print f
                    with zipfile.ZipFile(os.path.join(d,f)) as z:
                        shps = [s for s in z.namelist()
                                if os.path.splitext(s)[1] == '.shp']
                    for s in shps:
                        with fiona.open("/"+s,
                                        vfs="zip://"+os.path.join(d,f)
                        ) as src:
                            for p in src:
                                p['properties']['fname']=base
                                try:
                                    dst.write(p)
                                except Exception, e:
                                    print e
                elif ext == ".shp":
                    print f
                    with fiona.open(os.path.join(d,f)) as src:
                        for p in src:
                            p['properties']['fname']=base
                            try:
                                dst.write(p)
                            except Exception, e:
                                print e

if __name__ == "__main__":
    main(WORKING_DIRECTORY, OUT_SHP)
