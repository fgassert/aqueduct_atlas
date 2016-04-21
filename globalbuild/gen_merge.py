'''
Created on Oct 16, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import numpy as np
import matplotlib.mlab as mlab
from constants import *

def join_recs_on_keys(lhs, rhslist, keys):
    for arr in rhslist:
        for i in range(len(keys)+1):
            if i == len(keys):
                print "ERROR: failed to join %s" % (arr.dtype,)
            elif keys[i] in arr.dtype.names:
                #print "joining on %s" % keys[i]
                lhs = join_rec(lhs,keys[i],arr,keys[i])
                break
    return lhs


def join_rec(r1,field1,r2,field2):
    """1-to-1 joining with non-unique lefthand side keys"""
    mapping = dict(zip(r2[field2], range(len(r2))))
    diff = np.setdiff1d(r1[field1],r2[field2])
    r2len = len(r2)
    if len(diff) > 0:
        print "WARNING: %s no matching key: %s" % (field2, diff)
        for i in range(len(diff)):
            mapping[diff[i]]=r2len
    r2copy = mlab.rec_drop_fields(r2, (field2,))
    r2copy.resize(r2len+1)
    joinfields = list(r2copy.dtype.names)
    dtypes = []
    for i in range(len(joinfields)):
        if r2copy.dtype[i].kind == "i":
            dtypes.append(np.double)
        else:
            dtypes.append(r2copy.dtype[i])
        if r2copy.dtype[i].kind == "f":
            r2copy[r2copy.dtype.names[i]][-1]=NULL_VALUE
        while joinfields[i] in r1.dtype.names:
            joinfields[i] = joinfields[i]+"_"
    rightrec = r2copy[[mapping[key] for key in r1[field1]]]
    r1 = mlab.rec_append_fields(r1, joinfields, [rightrec[n] for n in rightrec.dtype.names], dtypes)
    return r1

def arrange_vector_by_ids(v,start_ids,end_ids,nodata=0):
    """
    Returns the values of a vector or rows of an array with start_ids mapped to end_ids
    
    Such that:
        the return array[i] is the value of v where start_ids==end_ids[i]
        if end_ids[i] is not in start_ids, array[i] is set to nodata
    """
    if len(start_ids)==len(end_ids) and all(start_ids == end_ids):
        return v
    mapping = dict(zip(start_ids, range(len(start_ids))))
    
    v_copy = v.copy()
    v_copy.resize(len(v)+1)
    v_copy[-1] = nodata
    idx = []
    for k in end_ids:
        if k in mapping:
            idx.append(mapping[k])
        else:
            idx.append(-1)
    return v_copy[idx]

def main():
    inputlist = ["bin/global_BWS_20121015.csv","bin/global_WRI_20121015.csv"]
    lhs = mlab.csv2rec("bin/global_GU_20121015.csv")
    rhslist = []
    for x in inputlist:
        rhslist.append(mlab.csv2rec(x))
    
    rhslist[0]["basinid"] = rhslist[0]["basinid"].astype(np.long)
    keys = ("basinid","countryid","id")
    lhs = join_recs_on_keys(lhs,rhslist,keys)
    mlab.rec2csv(lhs,"bin/test.csv")
    print "complete"

if __name__ == '__main__':
    main()
