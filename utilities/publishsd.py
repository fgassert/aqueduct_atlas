'''
Created on Sep 5, 2012

@author: francis.gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import os

BASEPATH = "C:/Users/francis.gassert/Desktop/export"

timestamp = "20120904"

OUTNAME = "aqueduct_global_test_%s" % timestamp
# 5. output database name <*.gdb>
INDB = OUTNAME + ".gdb"
# 6. mxd and msd names
MXDNAME = OUTNAME + ".mxd"

# map server connection file (.ags)
SERVICE_CON = '23_21_100_32.ags'
REGISTERED_FOLDER = "C:/arcgisstaging/"
FORCE_MANUAL_UPLOAD = True
# map server folder location
SERVER_FOLDER = 'Aqueduct'
PUBLISH = True
START = False

def publishsd(basepath, inmxd, indb, outname, service_con, server_folder=None, force_manual_upload=True, registered_folder=None, publish=True, start=True):
    print "making map service draft"
    ap.env.overwriteOutput = True
    ap.env.workspace = basepath
    outdb = outname + ".gdb"
    mxdname = outname + ".mxd"
    sddraft = outname + ".sddraft"
    sdname = outname + ".sd"
    
    
    mxd = ap.mapping.MapDocument(os.path.join(basepath,inmxd))
    
    if registered_folder == None:
        registered_folder = basepath
    
    if force_manual_upload and basepath != registered_folder:   
        layers = ap.mapping.ListLayers(mxd)
        print "copying geodatabase"
        ap.CreateFileGDB_management(registered_folder, outdb)
        ap.env.workspace = os.path.join(registered_folder, outdb)
        for l in layers:
            print "copying %s" % l.datasetName
            ap.CopyFeatures_management(l.dataSource,l.datasetName)
        print "copying mxd"
        mxd.saveACopy(os.path.join(registered_folder,mxdname))
        mxd = ap.mapping.MapDocument(os.path.join(registered_folder,mxdname))
        mxd.replaceWorkspaces(os.path.join(basepath, indb), "FILEGDB_WORKSPACE", os.path.join(registered_folder, indb), "FILEGDB_WORKSPACE")
        mxd.save()
        
    
    print "preparing service definition draft"
    analysis = ap.mapping.CreateMapSDDraft(mxd, sddraft, outname, 'ARCGIS_SERVER', service_con, None, server_folder)

    for k,v in analysis.iteritems():
        print "----%s----" % k
        for i,j in v.iteritems():
            print "%s %s" % (i, j) 
        
    if analysis['errors'] != {}:
        raise
    elif force_manual_upload and (u"Layer's data source is not registered with the server and data will be copied to the server", 24011) in analysis['messages']:
        raise Exception("Data not on server. Please copy data to server folder.")
    else:
        if publish:
            print "publishing map service"
            ap.StageService_server(sddraft, os.path.join(registered_folder,sdname))
            if start:
                s = "STARTED"
            else:
                s = "STOPPED"
            ap.UploadServiceDefinition_server(sdname, service_con, in_startupType=s)
            print "published"
        
if __name__ == "__main__":
    publishsd(BASEPATH, MXDNAME, INDB, OUTNAME, SERVICE_CON, SERVER_FOLDER, FORCE_MANUAL_UPLOAD, REGISTERED_FOLDER, PUBLISH, START)