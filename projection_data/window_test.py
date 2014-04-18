from ensemble_ops import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

WINDOWS = np.arange(11,51,5)
SYEAR = 1950
EYEAR = 2100

def main():
    out = [np.ones((len(WINDOWS),EYEAR-SYEAR+1))*np.nan for s in range(len(rcps))]
    for j in range(len(WINDOWS)):
        rcpidx = 0
        res = iter_models(interannual_cv, maf=csv_BT, pfx=ANNUAL, sfx=SFX, window=WINDOWS[j], syear=SYEAR, eyear=EYEAR)
        for s in range(len(rcps)):
            w = mdl_weights(s)            
            mean = res[rcpidx]*w[0]
            for i in range(1,len(w)):
                mean += res[i+rcpidx]*w[i]
            var = ((res[rcpidx]-mean)**2)*w[0]
            for i in range(1,len(w)):
                var += ((res[i+rcpidx]-mean)**2)*w[i]
            sd = np.sqrt(var)
            cv = sd/mean
            out[s][j,WINDOWS[j]//2:WINDOWS[j]//-2+1] = np.median(cv,0)
            rcpidx += len(w)
    df0 = pd.DataFrame(out[0])
    df1 = pd.DataFrame(out[1])

    df0.to_csv("rcp45_cv.csv")
    df1.to_csv("rcp85_cv.csv")

    plt.plot(df0.transpose())
    plt.show()
    plt.plot(df1.transpose())
    plt.show()

if __name__ == "__main__":
    main()
