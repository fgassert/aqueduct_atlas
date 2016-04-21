import time
import os

#TIMESTAMP = time.strftime("%Y%m%d",time.localtime())
TIMESTAMP = "20140214"

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/global_maps/"
os.chdir(CWD)
WORKSPACE = "global_workspace.gdb"

RAWBASINS = "global_inputs.gdb/global_basins_20140121"
BIGBASINS = "bigbasins_20140127"

BASINPOLY = "global_inputs.gdb/global_basins_named_20140127"
ADMINPOLY = "global_inputs.gdb/ne_10m_countries_20120902"
#ADMINPOLY = "global_inputs.gdb/isci_country_3_20120907"
LAKEPOLY = "global_inputs.gdb/ne_10m_majorlakes_20121116"
ADD_FEATURES = "global_inputs.gdb/ne_10m_addfeatures_20121122"

#GUPOLY = "global_inputs.gdb/global_GU_high_20121017"
#GUPOLY = "global_inputs.gdb/global_GU_med_20121107"
#GUPOLY = "global_inputs.gdb/global_GU_low_20121015"
GUPOLY = "global_GU_%s" % TIMESTAMP

#MXD_EXTRA_FEATURES = ["global_inputs.gdb/priority_env_20120229","global_inputs.gdb/ne_10m_admin0_bound_20120903","global_inputs.gdb/ne_10m_disputed_bound_20120903"]
MXD_EXTRA_FEATURES = None

MXD_TEMPLATE = "map_template_20120907.mxd"
MXD_TEMPLATE_INVERTED = "map_template_inverted_20120907.mxd"
MXD_TEMPLATE_EMPTY = "aqueduct_global_for_metadata_20140214.mxd"
MXD_TEMPLATE_AI = "aqueduct_global_for_ai_20140214.mxd"
LAYER_TEMPLATE = "basin_template_unique_20140214.lyr"
LAYER_TEMPLATE_HOLLOW = "hollow_20140214.lyr"
PRJNAME = "WGS 1984"
WEBPRJNAME = "WGS 1984 Web Mercator (Auxiliary Sphere).prj"

BASIN_ID_FIELD = "BasinID"
ADMIN_ID_FIELD = "CountryID"
GW_ID_FIELD = "AquiferID"
GU_FIELD = "GU"
COUNTRY_FIELD = "COUNTRY"
BASIN_NAME_FIELD = "BASIN_NAME"
NULL_VALUE = -32767

OUTPUT_GDB = "aqueduct_global_%s.gdb" % (TIMESTAMP)
#OUTPUT_GDB = "aqueduct_global_dl_%s.gdb" % (TIMESTAMP)
GLOBAL_OUT = "%s/global_master_%s" % (OUTPUT_GDB,TIMESTAMP)

ALL_FIELDS = [
              "BWS","BWS_s","BWS_cat",
              "WSV","WSV_s","WSV_cat",
              "SV","SV_s","SV_cat",
              "HFO","HFO_s","HFO_cat",
              "DRO","DRO_s","DRO_cat",
              "STOR","STOR_s","STOR_cat",
              "GW","GW_s","GW_cat",
              "WRI","WRI_s","WRI_cat",
              "ECO_S","ECO_S_s","ECO_S_cat",
              "MC","MC_s","MC_cat",
              "WCG","WCG_s","WCG_cat",
              "ECO_V","ECO_V_s","ECO_V_cat",
              "BA",
              "BT",
              "WITHDRAWAL",
              "CONSUMPTION",
              BASIN_NAME_FIELD,
              BASIN_ID_FIELD,
              COUNTRY_FIELD,
              GU_FIELD
              ]

MAP_FIELDS = [
              "BWS_cat",
              "WSV_cat",
              "SV_cat",
              "HFO_cat",
              "DRO_cat",
              "STOR_cat",
              "GW_cat",
              "WRI_cat",
              "ECO_S_cat",
              "MC_cat",
              "WCG_cat",
              "ECO_V_cat",
              ]

MAP_LABELS = [
              "BWS_cat",
              "WSV_cat",
              "SV_cat",
              "HFO_cat",
              "DRO_cat",
              "STOR_cat",
              "GW_cat",
              "WRI_cat",
              "ECO_S_cat",
              "MC_cat",
              "WCG_cat",
              "ECO_V_cat",
              ]

MAP_CLASSES = {
              "BWS_cat":("1. Low (<10%)","2. Low to medium (10-20%)","3. Medium to high (20-40%)","4. High (40-80%)","5. Extremely high (>80%)","Arid & low water use","No data"),
              "WSV_cat":("1. Low (<0.25)","2. Low to medium (0.25-0.5)","3. Medium to high (0.5-0.75)","4. High (0.75-1.0)","5. Extremely high (>1.0)","","No data"),
              "SV_cat":("1. Low (<0.33)","2. Low to medium (0.33-0.66)","3. Medium to high (0.66-1.0)","4. High (1.0-1.33)","5. Extremely high (>1.33)","","No data"),
              "HFO_cat":("1. Low (0-1)","2. Low to medium (2-3)","3. Medium to high (4-9)","4. High (10-27)","5. Extremely high (>27)","","No data"),
              "DRO_cat":("1. Low (<20)","2. Low to medium (20-30)","3. Medium to high (30-40)","4. High (40-50)","5. Extremely high (>50)","Desert regions","No data"),
              "STOR_cat":("1. High (>1)","2. High to medium (1-0.5)","3. Medium to low (0.5-0.25)","4. Low (0.25-0.12)","5. Extremely low (<0.12)","","No major reservoirs"),
              "GW_cat":("1. Low (<1)","2. Low to medium (1-5)","3. Medium to high (5-10)","4. High (10-20)","5. Extremely high (>20)","","No data"),
              "WRI_cat":("1. Low (<10%)","2. Low to medium (10-20%)","3. Medium to high (20-40%)","4. High (40-80%)","5. Extremely high (>80%)","Arid & low water use","No data"),
              "ECO_S_cat":("1. High (>40%)","2. High to medium (20-40%)","3. Medium to low (20-10%)","4. Low (10-5%)","5. Extremely low (<5%)","","No data"),
              "MC_cat":("1. Low (<0.05%)","2. Low to medium (0.05-0.1%)","3. Medium to high (0.1-0.2%)","4. High (0.2-0.4%)","5. Extremely high (0.4-0.8%)","","No data"),
              "WCG_cat":("1. Low (<2%)","2. Low to medium (2-5%)","3. Medium to high (5-10%)","4. High (10-20%)","5. Extremely high (>20%)","","No data"),
              "ECO_V_cat":("1. Low (0%)","2. Low to medium (1-5%)","3. Medium to high (5-15%)","4. High (15-35%)","5. Extremely high (35-100%)","","Fewer than two species")
               }

#WEIGHTING_SCHEMES = None
WEIGHTING_SCHEMES = {

                        "DEFAULT":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":2,
                        "HFO_s":4,
                        "DRO_s":4,
                        "STOR_s":8,
                        "GW_s":8,
                        "WRI_s":4,
                        "ECO_S_s":2,
                        "MC_s":4,
                        "WCG_s":8,
                        "ECO_V_s":2,
                        },
                        "DEF_PQUANT":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":2,
                        "HFO_s":4,
                        "DRO_s":4,
                        "STOR_s":8,
                        "GW_s":8,
                        },
                        "DEF_PQUAL":{
                        "WRI_s":4,
                        "ECO_S_s":2,
                        },
                        "DEF_REGREP":{
                        "MC_s":4,
                        "WCG_s":8,
                        "ECO_V_s":2,
                        },
                        "W_AGR":{
                        "BWS_s":16,
                        "WSV_s":8,
                        "SV_s":2,
                        "HFO_s":4,
                        "DRO_s":8,
                        "STOR_s":8,
                        "GW_s":8,
                        "WRI_s":2,
                        "ECO_S_s":1,
                        "MC_s":1,
                        "WCG_s":8,
                        "ECO_V_s":4,
                        },
                        "W_FOODBV":{
                        "BWS_s":8,
                        "WSV_s":4,
                        "SV_s":2,
                        "HFO_s":2,
                        "DRO_s":4,
                        "STOR_s":8,
                        "GW_s":4,
                        "WRI_s":8,
                        "ECO_S_s":4,
                        "MC_s":8,
                        "WCG_s":4,
                        "ECO_V_s":2,
                        },
                        "W_CHEM":{
                        "BWS_s":8,
                        "WSV_s":4,
                        "SV_s":4,
                        "HFO_s":4,
                        "DRO_s":16,
                        "STOR_s":4,
                        "GW_s":8,
                        "WRI_s":8,
                        "ECO_S_s":2,
                        "MC_s":16,
                        "WCG_s":16,
                        "ECO_V_s":8,
                        },
                        "W_POWER":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":8,
                        "HFO_s":4,
                        "DRO_s":16,
                        "STOR_s":4,
                        "GW_s":4,
                        "WRI_s":1,
                        "ECO_S_s":0,
                        "MC_s":2,
                        "WCG_s":2,
                        "ECO_V_s":8,
                        },
                        #"W_POW_QUAN":{
                        #"BWS_s":16,
                        #"WSV_s":4,
                        #"SV_s":8,
                        #"HFO_s":4,
                        #"DRO_s":16,
                        #"STOR_s":4,
                        #"GW_s":4,
                        #},
                        #"W_POW_QUAL":{
                        #"WRI_s":1,
                        #"ECO_S_s":0,
                        #},
                        #"W_POW_RR":{
                        #"MC_s":2,
                        #"WCG_s":2,
                        #"ECO_V_s":8,
                        #},
                        "W_SEMICO":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":4,
                        "HFO_s":4,
                        "DRO_s":4,
                        "STOR_s":8,
                        "GW_s":8,
                        "WRI_s":16,
                        "ECO_S_s":8,
                        "MC_s":8,
                        "WCG_s":4,
                        "ECO_V_s":8,
                        },
                        "W_OILGAS":{
                        "BWS_s":4,
                        "WSV_s":2,
                        "SV_s":2,
                        "HFO_s":2,
                        "DRO_s":4,
                        "STOR_s":4,
                        "GW_s":16,
                        "WRI_s":1,
                        "ECO_S_s":0,
                        "MC_s":16,
                        "WCG_s":16,
                        "ECO_V_s":4,
                        },
                        "W_MINE":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":4,
                        "HFO_s":16,
                        "DRO_s":2,
                        "STOR_s":4,
                        "GW_s":16,
                        "WRI_s":4,
                        "ECO_S_s":1,
                        "MC_s":16,
                        "WCG_s":16,
                        "ECO_V_s":4,
                        },
                        "W_CONSTR":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":2,
                        "HFO_s":4,
                        "DRO_s":4,
                        "STOR_s":8,
                        "GW_s":8,
                        "WRI_s":4,
                        "ECO_S_s":2,
                        "MC_s":2,
                        "WCG_s":4,
                        "ECO_V_s":1,
                        },
                        "W_TEX":{
                        "BWS_s":16,
                        "WSV_s":4,
                        "SV_s":2,
                        "HFO_s":4,
                        "DRO_s":4,
                        "STOR_s":8,
                        "GW_s":8,
                        "WRI_s":8,
                        "ECO_S_s":2,
                        "MC_s":4,
                        "WCG_s":8,
                        "ECO_V_s":2,
                        },
                        }

MINSCORE = 0
MAXSCORE = 5
MISC_CAT = 6
NODATA_CAT = 7
MAPRES=150
EXPORTAI=True

#####
GU_OUT = "global_GU_%s" % (TIMESTAMP)
GU_TOLERANCE = 0
GU_DICE = False

BASINCSV = "basins_15006.csv"

RUNOFFCSV = "global-GLDAS-2.0_Noah-3.3_M.020-20121211-filled-20130821-RO.csv"
BTCSV = "global-GLDAS-2.0_Noah-3.3_M.020-20121211-filled-20130821-Bt.csv"
BACSV = "global-GLDAS-2.0_Noah-3.3_M.020-20121211-filled-20130821-Ba.csv"
BTMONTHLYCSV = "global-GLDAS-2.0_Noah-3.3_M.020-20121211-monthly-filled-20130822-Bt.csv"
CONSUMPTIONCSV = "Ct_2010_20140121.csv"
AREACSV = "basin_area_20140121.csv"

WITHDRAWALCSV = "Ut_2010_20140121.csv"
BWS_OUT = "global_BWS_%s" % (TIMESTAMP)

WSV_OUT = "global_WSV_%s" % (TIMESTAMP)
SV_OUT = "global_SV_%s" % (TIMESTAMP)

FLOODPOLY = "global_inputs.gdb/FloodArchive_20111015"
HFO_OUT = "global_HFO_%s" % (TIMESTAMP)

AMPHIBPOLY = "global_inputs.gdb/SPECIES1109_DBO_VIEW_AMPHIBIANS_JOINED_20120625"
ECO_V_OUT = "global_ECO_V_%s" % (TIMESTAMP)

#DROUGHTRASTER = "global_inputs.gdb/d4plus_20120907"
DROUGHTRASTER2 = "global_inputs.gdb/dseverity_20120907"
DRO_OUT = "global_DRO_%s" % (TIMESTAMP)

GWRASTER = "gwfootprint.gdb/gwfootprint"
GWPOLY = "global_inputs.gdb/global_GW_20120922"
GW_OUT = "global_GW_%s" % (TIMESTAMP)

FANCONSCSV = "global-20121022-CFSR-filled-Use.csv"
WRI_OUT = "global_WRI_%s" % (TIMESTAMP)

PROTCSV = "global-GLDAS-2.0_Noah-3.3_M.020-20121211-filled-protected-20130828-Bt.csv"
ECO_S_OUT = "global_ECO_S_%s" % (TIMESTAMP)

STORAGECSV = "global-storage_20140121.csv"
STOR_FIELD = "CAP_MCM"
STORAGE_PTS = "global_inputs.gdb/grand_1_1_20140121"
STOR_OUT = "global_STOR_%s" % (TIMESTAMP)

MEDIACSV = "countries_MC_20120904.csv"
MC_OUT = "global_MC_%s" % (TIMESTAMP)

ACCESSCSV = "WHO2010WaterAccess20121018.csv"
WCG_OUT = "global_WCG_%s" % (TIMESTAMP)
