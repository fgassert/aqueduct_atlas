'''
Created on September 2, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import arcpy as ap
import numpy as np
import matplotlib.mlab as mlab
import histplotter
import os
from constants import *


class APGenerator(object):
    generator_name = "generator"
    plot_field_name = None
    map_layer_label = None
    threshold_values = (0,.1,.2,.4,.8,999999999999)
    c1 = .1
    base = 2
    category_names = None
    
    def __init__(self):
        pass
    
    def gen(self, output_file, *args, **kwargs):
        print "Initializing %s" % self.generator_name
        
        #initialize arcpy and workspace
        ap.env.overwriteOutput = True
        if 'workspace' in kwargs:
            ap.env.workspace = kwargs['workspace']
        
        #determine if output file exists and write
        if 'overwrite' in kwargs:
            write = kwargs['overwrite']
        else: 
            write = False

        if not write:
            if not ap.Exists(output_file):
                print "Warning: %s does not exist; generating" % output_file
                write = True
        if write:
            self._make(output_file, *args, **kwargs)
        
        self._postprocess(output_file, *args, **kwargs)
        
        #_get output array
        outarr = self._get_array(output_file)
        
        #generate secondary outputs
        
        if 'make_csv' in kwargs:
            self.make_csv(kwargs.pop('make_csv'), outarr)
        if 'make_plot' in kwargs:
            self.make_plot(kwargs.pop('make_plot'), outarr, **kwargs)
        if 'make_map' in kwargs:
            self.make_map(kwargs.pop('make_map'), output_file, **kwargs)
            
        #return array
        print "Completed %s" % self.generator_name        
        return outarr
        
    def _make(self, output_file, *args, **kwargs):
        """Performs necessary calculations and geospatial operations to generate output_file"""
        pass

    def _postprocess(self, output_file, *args, **kwargs):
        """Performs secondary calculations"""
        pass

    def _get_array(self, output_file, fields=None, null_value=None):
        """Retrieves output array as NumPy Record Array"""
        if null_value is None:
            null_value = NULL_VALUE
        if fields is not None:
            return ap.da.FeatureClassToNumPyArray(output_file, fields, null_value=null_value)

    def score(self, raw, logscale=True, invert=False, c1=None, base=None):
        print "scoring"
        if c1 is None:
            c1 = self.c1
        if base is None:
            base = self.base
        if logscale:
            score = (np.log(raw)-np.log(c1))/np.log(base)
        else:
            score = (raw-c1)/base
        if invert:
            score = -score
        score = score+1
        score[score<MINSCORE] = MINSCORE
        score[score>MAXSCORE] = MAXSCORE
        return score
        
    def categorize(self, score, miscmask=None):
        score = np.ceil(score)
        score[score==MINSCORE] = np.floor(MINSCORE+1)
        score[np.isnan(score)] = NODATA_CAT
        if miscmask is not None:
            score[miscmask] = MISC_CAT
        if self.category_names is not None:
            cnames = np.array(self.category_names)[score.astype(np.int)-1]
        else:
            cnames = score.astype(np.str)
        return cnames

    def make_csv(self, out_csv, array):
        if out_csv is None:
            return 0
        else:
            print "Generating csv"
            mlab.rec2csv(array, out_csv)
            return 1
            
    def make_plot(self, make_plot, plot_array, plot_field_name=None, plot_minvalue = None, plot_maxvalue = None, plot_log=False, plot_log_plus=0, **kwargs):
        
        if plot_array.dtype.names is None:
            if plot_array.ndim == 1:
                histvar = plot_array
            else:
                histvar = plot_array[:,-1]
        else:
            if plot_field_name is None:
                if self.plot_field_name is None:
                    return 0
                else:
                    histvar = plot_array[self.plot_field_name]
            else:
                histvar = plot_array[plot_field_name]
        print "Plotting"
        
        if plot_minvalue is not None:
            histvar = histvar[histvar>=plot_minvalue]
        if plot_maxvalue is not None:
            histvar = histvar[histvar<=plot_maxvalue]
        if plot_log:
            histvar = np.log(histvar+plot_log_plus)
        histvar = histvar[np.isfinite(histvar)]
        histplotter.hist(histvar, make_plot)
        return 1
        
    def make_map(self, make_map, output_layer, map_field=None, map_layer_label=None, map_values=None, map_labels=None, **kwargs):
        if map_field is None:
            map_field = self.plot_field_name
        if map_field is None:
            map_field = ap.Describe(output_layer).OIDFieldName
        print "Generating map"
        if map_values is None:
            map_values = self.threshold_values
        if map_values[0]>map_values[-1]:
            map_values = map_values[::-1]
            mxd = ap.mapping.MapDocument(MXD_TEMPLATE_INVERTED)
        else:
            mxd = ap.mapping.MapDocument(MXD_TEMPLATE)
        df = ap.mapping.ListDataFrames(mxd)[0]
        if map_layer_label is None:
            if self.map_layer_label is None:
                map_layer_label = os.path.basename(output_layer)
            else:
                map_layer_label = self.map_layer_label

        lyr = ap.mapping.ListLayers(mxd, "template", df)[0]
        #lyr = ap.mapping.Layer(LAYER_TEMPLATE)
        lyr.replaceDataSource(ap.env.workspace, "FILEGDB_WORKSPACE", output_layer, True)
        lyr.name = map_layer_label
        lyr.symbology.valueField = map_field
        lyr.symbology.classBreakValues = map_values
        if map_labels is not None:
            lyr.symbology.classBreakLabels = map_labels
        #ap.mapping.AddLayer(df, LAYER_TEMPLATE, layer_label)
        #df.extent = lyr.getExtent()
        print "Exporting map"
        ext = os.path.splitext(make_map)[1]
        if ext == '.jpg':
            ap.mapping.ExportToJPEG(mxd, make_map, resolution=MAPRES)
        elif ext == '.pdf':
            ap.mapping.ExportToPDF(mxd, make_map)
        elif ext == '.mxd':
            mxd.saveACopy(make_map)
        del mxd
        return 1
    