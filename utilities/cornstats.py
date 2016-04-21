
import pandas as pd
import os
import matplotlib.pyplot as plt
import sklearn.linear_model as lm
import sklearn.metrics as metrics
import numpy as np

CORNCSV = "county_corn_mean_20140305.csv"
IRRCSV = "corn_rasterstats.csv"

CWD = "C:/Users/francis.gassert/Documents/ArcGIS/GISSync/corn/"
os.chdir(CWD)

def logit(x):
    return np.log((x/(1-x)))
def invlogit(x):
    return 1/(1+np.e**-x)

def main():
    df = pd.read_csv(CORNCSV)
    df = df.set_index("ANSI")
    irr = pd.read_csv(IRRCSV)
    irr = irr.set_index("ANSI_MERGE")
    
    df = df.join(irr)
    print df.columns
    
    df["grainbiascorrect"] = df["grainirrbu"]/(df["grainirrbu"]+df["grainnonirrbu"])*df["grainbu"]
    df["silagebiascorrect"] = df["silageirrtons"]/(df["silageirrtons"]+df["silagenonirrtons"])*df["silagetons"]
    
    df["grainirrtons"] = df["grainbiascorrect"] * 0.0254
    df["graintons"] = df["grainbu"] * 0.0254
    
    df["tons"] = df["graintons"] + df["silagetons"]
    df["irrtons"] = df["grainirrtons"] + df["silagebiascorrect"]
    
    df["pctirr"] = df["grainirrtons"]/df["graintons"]
    df["logitpctirr"] = logit(df["pctirr"])
    
    df["_pctirr"] = df["mirad_irr"] / df["all_corn_750"]
    df["_grainirrtons"] = df["_pctirr"] * df["graintons"]
    df["_nirr"] = (1-df["_pctirr"]) * df["graintons"]
    df["_logitpctirr"] = logit(df["_pctirr"])
    
    
    
    
    fit = df.dropna(subset=["pctirr","_pctirr","grainirrtons","graintons"])
    fit = fit.drop(fit.ix[[8125,8000]].index,0)
    
    for a in np.logspace(0,1,100):
        print a, metrics.r2_score(fit["pctirr"],a*fit["_pctirr"]/((a-1)*fit["_pctirr"]+1))
    for a in np.logspace(0,1,100):
        print a, metrics.r2_score(fit["grainirrtons"],a*fit["_pctirr"]/((a-1)*fit["_pctirr"]+1)*fit["graintons"])
        print np.sum(a*fit["_pctirr"]/((a-1)*fit["_pctirr"]+1)*fit["graintons"])/np.sum(fit["grainirrtons"])

    #df["_grainnirrtons"] = 1 - df["_grainirrtons"]
    #df["_grainnirrtonsai"] = df["_grainnirrtons"]*np.log(df["mean_ai"]/10000.0)
    #df["mirad_nirr"] = df["all_corn"] - df["mirad_irr"]
    #df["mirad_nirrai"] = df["mirad_nirr"]*np.log(df["mean_ai"]/10000.0)
    
    #fit = df.dropna(subset=["grainirrtons","mirad_irr","all_corn_750"])
    
    #predictors = [["_grainirrtons","_grainnirrtons"],["_grainirrtons","_grainnirrtons","_grainnirrtonsai"],["mirad_irr","mirad_nirr"],["mirad_irr","mirad_nirr","mirad_nirrai"]]
    """
    predictors = [["_logitpctirr"]]

    clf = lm.LinearRegression(fit_intercept=True)
    for i in range(len(predictors)):
        clf.fit(fit[predictors[i]],fit["logitpctirr"])
        print "Predicting grain production"
        print predictors[i],
        print "Coefficients:"
        print clf.intercept_, clf.coef_
        print "R2: %s" % clf.score(fit[predictors[i]],fit["logitpctirr"])
        df["predirr"] = invlogit(clf.predict(df[predictors[i]]))
        print max(df["predirr"])
        score = df.dropna(subset=["grainirrtons"])
        plt.scatter(score["grainirrtons"],score["predirr"]*score["graintons"])
        plt.show()
        df["grain%s"%i] = np.sum(df[predictors[i]] * clf.coef_, 1)
        print "Total production: %s" % np.sum(df["grain%s" % i].dropna())    
    
    df.to_csv("pred.csv")
    """

if __name__ == "__main__":
    main()