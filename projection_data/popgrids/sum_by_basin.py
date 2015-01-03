import rasterstats
import pandas as pd

tifs = ["A2pa2000_5min.tif",
        "A2pa2010_5min.tif",
        "A2pa2020_5min.tif",
        "A2pa2030_5min.tif",
        "A2pa2040_5min.tif",
        "B2pa2000_5min.tif",
        "B2pa2010_5min.tif",
        "B2pa2020_5min.tif",
        "B2pa2030_5min.tif",
        "B2pa2040_5min.tif"]

inshp = '../shps/Basins_15006-20130820.shp'

def main():
    for t in tifs:
        stats = rasterstats.zonal_stats(inshp,t,stats=['sum'],copy_properties=True)
        df = pd.DataFrame(stats)
        df.set_index("BasinID",inplace=True)
        df.sort_index(inplace=True)
        df.to_csv(t[:-4]+'.csv')

if __name__ == "__main__":
    main()
