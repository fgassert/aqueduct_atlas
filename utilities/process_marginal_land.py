'''
Created on Aug 28, 2013

@author: francis.gassert
'''

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
from arcpy.sa import Raster, Con
import os

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/marginal_lands/"
os.chdir(CWD)

INPUTS = "marginal_land_inputs.gdb"
WORKSPACE = "scratch2.gdb"

SLOPE = os.path.join(INPUTS,"hislope_norm")
SOIL = os.path.join(INPUTS,"dsmw_norm")
ARID = os.path.join(INPUTS,"ai_05_norm")
IRR = os.path.join(INPUTS,"aai_data_norm")
AG = os.path.join(INPUTS,"crop_or_pasture_norm")
HA = os.path.join(INPUTS,"c5min_ha")
COUNTRIES = os.path.join(INPUTS,"mena_plus")


RO_CH = os.path.join(INPUTS,"RO_ch_85_50")
RO_45_30 = "RO_ch_rcp45_2030"
RO_85_30 = "RO_ch_rcp85_2030"
RO_45_50 = "RO_ch_rcp45_2050"
RO_85_50 = "RO_ch_rcp85_2050"
AI_CH = [RO_45_30,RO_85_30,RO_45_50,RO_85_50]
AI = os.path.join(INPUTS,"ai_yr")


def climate_ai(ch):
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    ap.CheckOutExtension("SPATIAL")

    print "generating %s_05" % ch    
    ai = Raster(AI)    
    ap.PolygonToRaster_conversion(RO_CH, ch, ch, cellsize=0.083333333)
    ro_ch = Raster(ch)
    ai_t = Con((ai * ro_ch)<=5000,1,0)
    ai_out = "%s_05" % ch
    ai_t.save(ai_out)
    return ai_out

def calc_rasters(ai):
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    ap.CheckOutExtension("SPATIAL")
    
    print "calculating land distribution"
    slope = Raster(SLOPE)
    soil = Raster(SOIL)
    arid = Raster(ai)
    irr = Raster(IRR)
    ag = Raster(AG)
    ha = Raster(HA)
    
    land_constrained = Con(slope>soil,slope,soil)
    water_constrained = Con(arid<irr,0,arid-irr)
    both_constrained = land_constrained * water_constrained
    
    landonly_constrained = land_constrained - both_constrained
    wateronly_constrained = water_constrained - both_constrained
    
    ag_both_constrained = ag * both_constrained
    ag_landonly_constrained = ag * landonly_constrained
    ag_wateronly_constrained = ag * wateronly_constrained
    ag_marginal = ag * (landonly_constrained + water_constrained)
    ag_favored = ag - ag_marginal
    
    ag_both_constrained.save("ag_both_constrained")
    ag_landonly_constrained.save("ag_landonly_constrained")
    ag_wateronly_constrained.save("ag_wateronly_constrained")
    ag_marginal.save("ag_marginal")
    ag_favored.save("ag_favored")
    
    both_ha = ag_both_constrained * ha
    landonly_ha = ag_landonly_constrained * ha
    wateronly_ha = ag_wateronly_constrained * ha
    marginal_ha = ag_marginal * ha
    favored_ha = ag_favored * ha
    
    both_ha.save("ag_both_cons_ha_%s"%ai)
    landonly_ha.save("ag_landonly_cons_ha_%s"%ai)
    wateronly_ha.save("ag_wateronly_cons_ha_%s"%ai)
    marginal_ha.save("ag_marginal_ha_%s"%ai)
    favored_ha.save("ag_favored_ha_%s"%ai)
    

def get_stats(ch):
    print "calculating statistics %s" % ch
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    ap.CheckOutExtension("SPATIAL")
    ap.sa.ZonalStatisticsAsTable(COUNTRIES,"name","ag_both_cons_ha_%s"%ch,"ag_both","DATA","SUM")
    ap.sa.ZonalStatisticsAsTable(COUNTRIES,"name","ag_wateronly_cons_ha_%s"%ch,"ag_wat","DATA","SUM")
    ap.sa.ZonalStatisticsAsTable(COUNTRIES,"name","ag_landonly_cons_ha_%s"%ch,"ag_land","DATA","SUM")
    ap.sa.ZonalStatisticsAsTable(COUNTRIES,"name","ag_favored_ha_%s"%ch,"ag_fav","DATA","SUM")
    
    both = ap.da.TableToNumPyArray("ag_both",["name","SUM"])
    wat = ap.da.TableToNumPyArray("ag_wat",["name","SUM"])
    land = ap.da.TableToNumPyArray("ag_land",["name","SUM"])
    fav = ap.da.TableToNumPyArray("ag_fav",["name","SUM"])
    
    rec = np.rec.fromarrays([both["name"],both["SUM"],wat["SUM"],land["SUM"],fav["SUM"]],names=('name','both','wat','land','fav'))
    mlab.rec2csv(rec,"%s.csv"%ch)
    

def main():
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
    ap.CopyRaster_management(ARID,"ai05")
    calc_rasters("ai05")
    get_stats("ai05")
    for r in AI_CH:
        ai = climate_ai(r)
        calc_rasters(ai)
        get_stats(ai)
    
if __name__ == '__main__':
    main()
    
    
    
    
WORKSPACE = "scratch.gdb"
SOILS = "dsmw"

def makesoils():
    print "initializing"
    ap.env.overwriteOutput = True
    ap.env.workspace = WORKSPACE
    
    ap.CopyFeatures_management(os.path.join(INPUTS,SOILS),SOILS)
    soilfield = 'DOMSOI'
    soil_categories = {  1:['Z','Zg','Zt','Zm','Zo','SALT'],
                        2:['S','Sg','Sm','So','Ws'],
                        3:['I','E','U','ROCK'],
                        4:['DS','Qa'],
                        4.1:['Ql','Qf','Qc'], #Ql Qf Qc in arid only
                        5:['R','Rx','Rc','Rd','Re'],
                        6:['W','Wm','Wh','Wd','We'],
                        7:['F','Fp','Fa','Fr','Fx','Fo','A','Ap','Ag','Af','P','Pp','Pg','Ph','Ph','Pf','Pl','Po','D','Dg','Dg','Dd','De'],
                        8:['O','Ox','Od','Oe','Gx','Gp'],
                        9:['Jt']
    }
    soil_names = {
        0:'Good',
        1:'Saline',
        2:'Salty',
        3:'Shallow',
        4:'Sandy',
        4.1:'Sandy (if arid)',
        5:'Poor profile',
        6:'Structure/texture limitations',
        7:'Acidic, infirtile, toxic',
        8:'Wetland',
        9:'Acid sulfate'
    }
    soil_list = []
    soil_values = []
    soil_labels = []
    for k,v in soil_categories.iteritems():
        for t in v:
            soil_list.append(t)
            soil_values.append(k)
            soil_labels.append(soil_names[k])
    sarr = np.rec.fromarrays([soil_list,soil_values,soil_labels],names=[soilfield,"CATEGORY","LABEL"])
    mlab.rec2csv(sarr,'soil_categories.csv')
    print sarr[soilfield]
    ap.da.ExtendTable(os.path.join(CWD,WORKSPACE,SOILS),soilfield,sarr,soilfield)
            
            
    print "complete"