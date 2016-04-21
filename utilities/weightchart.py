from svg import *
import numpy as np
import random
import subprocess, time

CHART_WIDTH = 550
CHART_HEIGHT = 300
CHART_COLORS = ["#FFE600","#FF9900","#FF1900","#808073"]
#CHART_COLORS = ["#FFE600","#FF1900","#BB0010","#808073"]
CHART_POS = (80,40)
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
H_SPACING = 14
VERTICAL_DIV_COLOR = "#FFFFFF"
VERTICAL_DIV_WIDTH = 0
HORIZONTAL_DIV_COLOR = "#FFFFFF"
HORIZONTAL_DIV_WIDTH = 1
AXIS_COLOR = "black"
AXIS_WIDTH = 2
AXIS_EXTENTION = 1
TICK_LENGTH = 5
TICK_WIDTH = 1
TICK_COLOR = "black"
YAXIS_TICKS = 5
FONTSIZE = 24
FONTNAME = "Arial MT Std"
savename = "bin/test_chart.svg"
INKSCAPE_PATH = r"C:\Users\francis.gassert\AppData\Local\inkscape\inkscape.exe"
RESOLUTION = 150



TITLE = "Indicators by weight"
Y_LABEL = "Percentage of total capacity"
LEGEND_LABELS = ["Low to medium (0&#x2013;3)","High (3&#x2013;4)","Extremely high (4&#x2013;5)","No data"]
INDICATOR_NAMES = ["Baseline water stress","Interannual variability","Seasonal variability","Flood","Drought","Upstream storage","Groundwater","Return flow","Protected land","Media coverage","Access to water","Threatened amphibians"]

def gen_square_chart(weights, densities, savename, names=None):
    """docstring for main"""
    
    if names is None:
        names = INDICATOR_NAMES
        
    while weights.count(0):
        x = weights.index(0)
        weights.pop(x)
        names.pop(x)
        densities.pop(x)
        
    
    weights = np.array(weights, dtype=np.double)
    pweights = weights/np.sum(weights)
    colwidth = pweights*(CHART_WIDTH-H_SPACING*len(weights))
    colheights = []
    for c in densities:
        c = np.array(c, dtype=np.double)
        pc = c/np.sum(c)
        colheights.append(pc*CHART_HEIGHT)
    
    
    a = svg(IMAGE_WIDTH,IMAGE_HEIGHT,viewbox='0 0 %s %s' % (IMAGE_WIDTH, IMAGE_HEIGHT))
    
    # MAKE CHART
    x = CHART_POS[0]+H_SPACING/2
    for i in range(len(colwidth)):
        y = CHART_HEIGHT+CHART_POS[1]
        w = colwidth[i]
        for j in range(len(colheights[i])):
            h = colheights[i][j]
            y = y - h
            a.add(rect(x,y,w,h,fill=CHART_COLORS[j]))
        x = x + w + H_SPACING
    
    #MAKE DIVIDERS and X_TICKS
    x = CHART_POS[0]
    for i in range(len(colwidth)):
        y = CHART_HEIGHT+CHART_POS[1]
        w = colwidth[i]
        
        if VERTICAL_DIV_WIDTH>0:
            a.add(line(x,y,x,y-CHART_HEIGHT,stroke=VERTICAL_DIV_COLOR,strokewidth=VERTICAL_DIV_WIDTH))
        if TICK_WIDTH>0:
            a.add(line(x,y,x,y+TICK_LENGTH,stroke=TICK_COLOR,strokewidth=TICK_WIDTH))
            a.add(text(names[i], x+(w+H_SPACING+FONTSIZE)/2, y+TICK_LENGTH+FONTSIZE/2, fontfamily=FONTNAME, fontsize=FONTSIZE, p='transform="rotate(-45,%s,%s)" style="text-anchor: end"'%(x+(w+H_SPACING+FONTSIZE)/2, y+TICK_LENGTH+FONTSIZE/2)))
            if pweights[i]>.01:
                a.add(text("%3.0f%%" % round(pweights[i]*100), x+(w+H_SPACING)/2, CHART_POS[1]-FONTSIZE/2, fontfamily=FONTNAME, fontsize=FONTSIZE, p='style="text-anchor: middle"'))
        if HORIZONTAL_DIV_WIDTH>0:
            y = CHART_HEIGHT+CHART_POS[1]-colheights[i][0]
            for j in range(1,len(colheights[i])):
                h = colheights[i][j]
                a.add(line(x+H_SPACING/2,y,x+w+H_SPACING/2,y,stroke=HORIZONTAL_DIV_COLOR, strokewidth=HORIZONTAL_DIV_WIDTH))
                y = y - h
        x = x + w + H_SPACING
      
    #MAKE Y_TICKS AXIS  
    x = CHART_POS[0]
    y = CHART_HEIGHT+CHART_POS[1]
    if TICK_WIDTH>0:
        for j in range(YAXIS_TICKS+1):
            ty = y-(j/float(YAXIS_TICKS)*CHART_HEIGHT)
            a.add(line(x,ty,x-TICK_LENGTH,ty,stroke=TICK_COLOR,strokewidth=TICK_WIDTH))
            a.add(text("%3.0f%%" % round(j*100/YAXIS_TICKS), x-TICK_LENGTH-FONTSIZE/2, ty+FONTSIZE/2.4, fontfamily=FONTNAME, fontsize=FONTSIZE, p='style="text-anchor: end"'))
    a.add(line(x,y,x,y-CHART_HEIGHT-AXIS_EXTENTION,stroke=AXIS_COLOR,strokewidth=AXIS_WIDTH))
    a.add(line(x,y,x+CHART_WIDTH+AXIS_EXTENTION,y,stroke=AXIS_COLOR,strokewidth=AXIS_WIDTH))
        
    #MAKE LEGEND
    x = CHART_POS[0]
    #y = CHART_POS[1]-3*FONTSIZE
    y = CHART_POS[1]+CHART_HEIGHT+100
    for i in range(len(LEGEND_LABELS)):
        a.add(rect(x,y,FONTSIZE,FONTSIZE,fill=CHART_COLORS[i]))
        x = x + FONTSIZE * 1.5
        a.add(text(LEGEND_LABELS[i], x, y+FONTSIZE/1.2, fontfamily=FONTNAME, fontsize=FONTSIZE, p='style="text-anchor: start"'))
        x = x + len(LEGEND_LABELS[i])*FONTSIZE/2.4
        
    gen(a, "%s.svg" % savename, False)
    
    proc = []
    
    params = [INKSCAPE_PATH,"-f", "%s.svg" % savename, "-e", "%s.png" % savename, "-d", "%s" % RESOLUTION]
    proc.append(subprocess.Popen(params))
    
    while len(proc)>0:
        i=0
        while i < len(proc):
            if proc[i].poll() is not None:
                proc.pop(i)
            else:
                i=i+1
        time.sleep(.5)


if __name__ == '__main__':
    #weights = [16,4,2,4,4,8,8,4,2,4,8,2]
    #densities = [[random.random() for i in range(2,5)] for i in range(len(weights))]
    weights = [16,4,8,4,16,4,4,1,.5,2,2,8]
    densities = [[0.3663,0.2301,0.4036,0.0000],
        [0.7606,0.1273,0.1121,0.0000],
        [0.7584,0.1882,0.0535,0.0000],
        [0.4456,0.4385,0.1159,0.0000],
        [0.9549,0.0417,0.0033,0.0000],
        [0.3856,0.1510,0.1072,0.3561],
        [0.2647,0.0162,0.1241,0.5951],
        [0.4954,0.0869,0.4177,0.0000],
        [0.0066,0.0162,0.9772,0.0000],
        [1.0000,0.0000,0.0000,0.0000],
        [1.0000,0.0000,0.0000,0.0000],
        [0.9163,0.0825,0.0012,0.0000]]
    savename = "bin/powercap"
    #gen_square_chart(weights,densities,savename)
    weights = [16,4,8,4,16,4,4,1,.5,2,2,8]
    densities = [[0.3484,0.2323,0.4193,0.0000],
        [0.7450,0.1360,0.1190,0.0000],
        [0.7394,0.2153,0.0453,0.0000],
        [0.4278,0.4561,0.1161,0.0000],
        [0.9405,0.0538,0.0057,0.0000],
        [0.4023,0.1416,0.1020,0.3541],
        [0.2436,0.0227,0.1133,0.6204],
        [0.4646,0.0907,0.4448,0.0000],
        [0.0085,0.0170,0.9745,0.0000],
        [1.0000,0.0000,0.0000,0.0000],
        [1.0000,0.0000,0.0000,0.0000],
        [0.9207,0.0765,0.0028,0.0000]]
    savename = "bin/powerplant"
    #gen_square_chart(weights,densities,savename)
    weights = [16,4,2,4,4,8,8,4,2,4,8,2]
    densities=[[0,28,33,78],
        [4,5,8,122],
        [4,4,20,111],
        [0,11,74,54],
        [0,0,5,134],
        [35,43,17,44],
        [81,2,1,55],
        [0,23,17,99],
        [4,81,25,29],
        [0,5,3,131],
        [12,2,4,121],
        [1,7,10,121]]
    densities=[a[::-1] for a in densities]
    savename = "bin/pg20130123"
    gen_square_chart(weights,densities,savename)
    savename = "bin/pg_categories_20130123"
    weights = [11.5,1.5,3.5]
    densities=[[91,39,9,0],
        [75,43,21,0],
        [134,5,0,0]]
    gen_square_chart(weights,densities,savename,["Quantity","Quality","Regulatory/reputational"])
    
    weights = [4,1,2,1,4,1,1,.25,0,.5,.5,2]
    densities = [[24,20,13,0],
        [54,3,0,0],
        [56,1,0,0],
        [14,37,6,0],
        [57,0,0,0],
        [29,11,12,5],
        [23,0,0,34],
        [26,19,12,0],
        [0,0,0,57],
        [57,0,0,0],
        [57,0,0,0],
        [56,1,0,0]]
    savename = "bin/exelon20130125"
    gen_square_chart(weights,densities,savename)
    weights = [14,.25,3]
    densities=[[56,1,0,0],
        [26,19,12,0],
        [57,0,0,0]]
    savename = "bin/exelon_categories_20130125"
    gen_square_chart(weights,densities,savename,["Quantity","Quality","Regulatory/reputational"])
    
    