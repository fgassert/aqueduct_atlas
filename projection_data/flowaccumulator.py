"""
flowaccumulator.py

A simple basin to basin flow accumulation script

Requires numpy

Based on work by ISciences L.L.C.
http://isciences.com/

Copyright 2013 World Resources Institute

Licensed under the Creative Commons Attribution 4.0 International Public License (CC-BY 4.0)
http://creativecommons.org/licenses/by/4.0/
"""

import numpy as np

# maximum levels to accumulate before breaking
MAXLEVELS = 1000
VERBOSE = False

def dprint(s):
    if VERBOSE:
        print s

def accumulate(ids, d_ids, f0, f, *args):
    """
    Accumulates values over basins based on downstream relationships
    
    Parameters:
        ids:numpy.array     basin ids
        d_ids:numpy.array   id of basin which is immediately downstream of the given basin
        f0:function         function to compute values for basins without upstream basins
                            f0 must take at least one parameter:
                                i:int, the index of given basin within <ids> (this index in independent of the basin id,
                                   to retrieve the basin id, pass the <ids> array as an addition argument. ids[i] -> basin id
                            f0 must return a single numeric value
        f:function          function to compute values for basins with upstream basins
                            f must take at least three parameters:
                                i:int, the index of the given basin within <ids>
                                idx:numpy.array, boolean vector of indicating the basins immediately upstream of the given basin
                                values:numpy.array, computed values for all basins 
                                    values[idx] -> values of basins immediately upstream of the given basin
                            for simple flow accumulation, f should return ( sum(values[idx]) + f0(i, *args) )
                            f must return a single numeric value
        *args:arguments     [optional] additional arguments to pass through to f0 and f.
                            Both f0 and f must be able to accept the same additional arguments.
        
    Returns:
        numpy.array         accumulated basin values
        
    """
    return accumulate_vector(ids, d_ids, f0, f, 1, *args)
    
def accumulate_vector(ids, d_ids, f0, f, _len=1, *args):
    """
    Same as accumulate, but values is an m*n array where
        m = len(ids)
        n = _len
    Allows accumulation of vectors of values rather than single values
    f0 and f must return a 1d array-like of length _len
    """
    x = len(ids)
    dprint ("ids: %s" % x)
    
    computed = np.zeros(x,dtype=bool)
    if _len > 1:
        values = np.zeros((x,_len))
    else:
        values = np.zeros(x)
    
    # build upstream index array
    up_idx = np.empty((x,x),dtype=bool);
    for i in range(x):
        up_idx[i,:] = d_ids==ids[i]
    
    # no basins are upstream of the given basin
    no_upstream = ~np.any(up_idx, 1)
    
    # compute values for the basins with no upstream basins
    for i in np.arange(x)[no_upstream]:
        values[i] = f0(i, *args)
    computed[no_upstream] = 1
    
    level = 0
    while ~np.all(computed) and level<MAXLEVELS:
        
        dprint ("computed: %s/%s" % (np.sum(computed),x))
        
        # none of the uncomputed basins are upstream of the given basin
        up_computed = ~np.any(up_idx[:,~computed], 1)
        # and the given basin hasn't been computed yet
        to_compute = up_computed & ~computed
        
        # just compute the ones we need to
        for i in np.arange(x)[to_compute]:
            values[i] = f(i, up_idx[i,:], values, *args)
        computed[to_compute] = 1
        
        level +=1
    
    dprint ("longest path: %s" % level)
    
    return values

