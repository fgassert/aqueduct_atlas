#!/usr/bin/env python

import mapnik as mk
import cairo
import sys
import getopt

def render(input_file, output_file, width=800, height=800, bounds=None):
    m = mk.Map(width, height)
    mk.load_map(m, input_file, False)
    if bounds is not None:
        bbox = m.Envelope(*bounds)
        m.zoom_to_box(bbox)
    else:
        m.zoom_all()
    
    if output_file[-4:] in ['.png','.tif','.jpg']:
        mk.render_to_file(m, output_file)
    elif output_file[-4:] == '.pdf':
        s = cairo.PDFSurface(output_file, width, height)
        mk.render(m, s)
        s.finish()
    elif output_file[-4:] == '.svg':
        s = cairo.SVGSurface(output_file, width, height)
        mk.render(m, s)
        s.finish()
    else:
        print "Error: output file extension '{}' not understood".format(output_file)

def usage():
    print 'mapnik_render.py <mapnik.xml> <output_file> <width> <height> [options]'
    print ' Renders mapnik xml to output image, filetype inferred from extension. Filetypes supported: PNG, TIF, JPG, PDF, SVG'
    print ' Options:'
    print '  width, height   size of output_file in pixels or points (1/72") if pdf or svg'
    print '  -h              print this message and exit'
    print '  -b <left,bottom,right,top>'
    print '                  bounding box in map units'

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:],'hb:d:')
    
    args[2]=int(args[2])
    args[3]=int(args[3])
    
    bounds = None
    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit()
        elif o == '-b':
            bounds = a.split(',')
            if len(bounds) != 4:
                bounds = None

    render(*args, bounds=bounds)
