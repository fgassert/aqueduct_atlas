import rasterstats
import pandas as pd

tifs = ['2010_irr.tif',
        '2010_tot.tif',
        'wf_bltot_m3.tif']
inshp = '../shps/Basins_15006-20130820.shp'

def main():
    for t in tifs:
        stats = rasterstats.zonal_stats(inshp,t,stats=['sum'],copy_properties=True)
        df = pd.DataFrame(stats)
        df.set_index('BasinID',inplace=True)
        df.sort_index(inplace=True)
        df.to_csv(t[:-4]+'.csv')

if __name__ == "__main__":
    main()
