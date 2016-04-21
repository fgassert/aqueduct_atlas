'''
Created on Aug 20, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import matplotlib.pyplot as plt
import math

pltfigurenum = 0
VAR = []

def hist(var, save_name = None):
    if len(var)<3:
        print "too few observations to plot"
        return 0
    bins = int(math.log(len(var))*4-1)
    global pltfigurenum
    pltfigurenum += 1
    plt.figure(pltfigurenum)
    plt.hist(var, bins)
    if save_name is None:
        plt.show()
    else:
        plt.savefig(save_name)

if __name__ == "__main__":
    hist(VAR)