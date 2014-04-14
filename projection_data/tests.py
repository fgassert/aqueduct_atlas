
from ensemble_ops import *
import os
import pandas as pd
import numpy as np

def cv():
    mdl = mdls[0].keys()[0]
    rcp = rcps[0]
    run = mdls[0][mdl][0]
    tyear = 1990

    pfx = "monthly/"
    sfx = "_m-20140402"

    cv = intraannual_cv(csv_BT,t=tyear,mdl=mdl,rcp=rcp,run=run,pfx=pfx,sfx=sfx)
    
    test_bt = []
    for i in range(12):
        test_bt.append(csv_BT(t=tyear, mdl=mdl, rcp=rcp, run=run, pfx=pfx, sfx="%0.2d%s"%(i+1,sfx))[0])
    print "cv[0] is ", cv[0]
    print "should be", np.std(test_bt)/np.mean(test_bt)

def ma():
    mdl = mdls[1].keys()[0]
    rcp = rcps[1]
    run = mdls[1][mdl][0]
    tyear = 1990

    pfx = "annual/"
    sfx = "_m-20140402"

    ma = moving_average(csv_BT,mdl=mdl,rcp=rcp,run=run,pfx=pfx,sfx=sfx)

    test_bt = []
    for i in range(tyear-10,tyear+11):
        test_bt.append(csv_BT(t=i, mdl=mdl, rcp=rcp, run=run, pfx=pfx, sfx=sfx)[0])
    print "ma[0] is ", ma[tyear][0]
    print "should be", np.mean(test_bt)


def main():
    cv()
    ma()


if __name__ == "__main__":
    main()
