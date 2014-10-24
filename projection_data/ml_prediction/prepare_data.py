
import numpy as np
import pandas as pd
import sklearn.linear_model as lm
import sklearn.cross_validation as cv
import sklearn.preprocessing as pp
from constants import *

def polyFeatures(X,d=2):
    """"""
    m = X.shape[1]
    d2 = d+1
    j = np.arange(d2**m)
    p = np.empty((d2**m,m))
    labels = []
    for i in range(m):
        p[:,i]=np.mod(np.floor(j/d2**i),d2)
    idx = np.sum(p,1)<=d
    p = p[idx]
    
    poly = np.ones((len(X),len(p)))
    for i in range(len(p)):
        labels.append(polyLabels(X.columns,p[i]))
        poly[:,i] = np.prod(X**p[i,:],1)

    return pd.DataFrame(poly,X.index,labels)

def polyLabels(labels,idx):
    label = []
    for i in range(len(labels)):
        if idx[i]>1:
            label.append("%s^%d" % (labels[i],idx[i]))
        else:
            label.append(labels[i])
    return '.'.join(labels)

def prep_data():
    raw = pd.read_csv(DATACSV)
    proj = pd.read_csv(PROJCSV)
    full = raw.append(proj).reset_index()
    features = [GDP, POP, LAND, URB, BWSPOP, BWSNTL]
    full = full.dropna(subset=features)

    full[lnIND] = np.log(full[IND])
    full[lnDOM] = np.log(full[DOM])
    full[lnGDP] = np.log(full[GDP])
    full[lnPOP] = np.log(full[POP])
    full[lnLAND] = np.log(full[LAND])

    full[IND_GDP] = full[IND]/full[GDP]
    full[DOM_POP] = full[DOM]/full[POP]

    return full

def nKFold_score(X, y, clf, seed=1234567, xK=XK, nK=NK,  fit_params=None, verbose=0):
    np.random.seed(seed)
    S = np.empty(xK*nK)
    for i in range(xK):
        kf = cv.KFold(len(y), n_folds=nK, indices=False, shuffle=True)
        try:
            S[i*nK:(i+1)*nK] = cv.cross_val_score(clf, X, y, cv=kf, n_jobs=-1, verbose=verbose, fit_params=fit_params)
        except Exception as e:
            print "ERROR: ", type(e)
            if verbose:
                print e
    return S

def Xy_lnXdYRd_IND_GDP(train, d=2, YEARd=1, c=True, cYEAR=False):
    features = [lnGDP, lnPOP, lnLAND, URB, BWSNTL]
    X = polyFeatures(train[features],d)    #make d deg features
    
    if c:   #add country dummies
        c = pd.get_dummies(train[ISO])
        if cYEAR:
            cY = c.mul(train[YEAR],0)
            c = c.merge(cY, left_index=True, right_index=True)
        X = c.merge(X, left_index=True, right_index=True)

    for i in range(YEARd):
        X['%s%d'%(YEAR,i+1)] = train[YEAR]**(i+1)
        
    y = train[IND_GDP]

    scaler = pp.StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    return X,y

def main():    
    full = prep_data()
    train = full.dropna(subset=[IND,lnIND])

    nA = 50
    A = np.logspace(3,-1,nA)     #Generate alphas for ridge regression
    RCVclf = lm.RidgeCV(alphas=A,fit_intercept=True)
    BRclf = lm.BayesianRidge(fit_intercept=True)
    
    seed = 21328386381431

    X,y = Xy_lnXdYRd_IND_GDP(train,2,1,0)
    print 'Industrial/GDP <- X2 YEAR'
    S = nKFold_score(X,y,BRclf,seed)
    print ' Bayes Ridge:  mean r2 %5.3f, Median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    S = nKFold_score(X,y,RCVclf,seed)
    print ' Ridge LOO CV: mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))

    X,y = Xy_lnXdYRd_IND_GDP(train,3,1,0)
    print 'Industrial/GDP <- X3 YEAR'
    S = nKFold_score(X,y,BRclf,seed)
    print ' Bayes Ridge:  mean r2 %5.3f, Median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    S = nKFold_score(X,y,RCVclf,seed)
    print ' Ridge LOO CV: mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))

    X,y = Xy_lnXdYRd_IND_GDP(train,2,1,1)
    print 'Industrial/GDP <- X2 YEAR c'
    S = nKFold_score(X,y,BRclf,seed)
    print ' Bayes Ridge:  mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    S = nKFold_score(X,y,RCVclf,seed)
    print ' Ridge LOO CV: mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))

    X,y = Xy_lnXdYRd_IND_GDP(train,2,1,1,1)
    print 'Industrial/GDP <- X2 YEAR c cYEAR'
    S = nKFold_score(X,y,BRclf,seed)
    print ' Bayes Ridge:  mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    S = nKFold_score(X,y,RCVclf,seed)
    print ' Ridge LOO CV: mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))

    X,y = Xy_lnXdYRd_IND_GDP(train,3,1,1)
    print 'Industrial/GDP <- X3 YEAR c'
    S = nKFold_score(X,y,BRclf,seed)
    print ' Bayes Ridge:  mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    S = nKFold_score(X,y,RCVclf,seed)
    print ' Ridge LOO CV: mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    
    X,y = Xy_lnXdYRd_IND_GDP(train,3,1,1,1)
    print 'Industrial/GDP <- X3 YEAR c cYEAR'
    S = nKFold_score(X,y,BRclf,seed)
    print ' Bayes Ridge:  mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))
    S = nKFold_score(X,y,RCVclf,seed)
    print ' Ridge LOO CV: mean r2 %5.3f, median r2 %5.3f, Std r2 %5.3f' % (np.mean(S), np.median(S), np.std(S))

    #m3 = clfIND_GDPlnXdYRd(full,train,2,3)

if __name__ == "__main__":
    main()

if 0:
    #deadcode
    clf.fit(X,y)
    alpha = clf.alpha_
    clf = lm.Ridge(alpha=alpha,fit_intercept=True)
    clf.fit(X,y)
    s = pd.DataFrame(index=_X.columns)
    s['coef'] = clf.coef_
    s['magnitude'] = np.abs(s['coef'])*scaler.std_
    print s.sort('magnitude',ascending=False).head(20)
    print "alpha ", alpha
    print "train r2 ", clf.score(X,y)
    print "val r2   ", r2_score(yval,clf.predict(Xval))
    print "trainerr/valerr ", np.sum((clf.predict(X)-y)**2)/len(y)/2/(np.sum((clf.predict(Xval)-yval)**2)/len(yval)/2)
    for yr in range(2005,2080,5):
        print yr, np.sum(clf.predict(scaler.transform(_X[fullprep[YEAR]==yr][fullprep[SSP]=='SSP2']))*fullprep[fullprep[YEAR]==yr][fullprep[SSP]=='SSP2'][GDP])
    '''
    print "2005 OBS", np.sum(np.exp(clf.predict(Xo2005)))
    print "2005 ", np.sum(np.exp(clf.predict(X2005)))
    print "2010 ", np.sum(np.exp(clf.predict(X2010)))
    print "2020 ", np.sum(np.exp(clf.predict(X2020)))
    print "2030 ", np.sum(np.exp(clf.predict(X2030)))
    print "2040 ", np.sum(np.exp(clf.predict(X2040)))
    print "2050 ", np.sum(np.exp(clf.predict(X2050)))
    print "2060 ", np.sum(np.exp(clf.predict(X2060)))
    print "2070 ", np.sum(np.exp(clf.predict(X2070)))
    print "2080 ", np.sum(np.exp(clf.predict(X2080)))
    '''
    clf = lm.BayesianRidge(verbose=True,fit_intercept=True)
    clf.fit(X,y)
    s = pd.DataFrame(index=_X.columns)
    s['coef'] = clf.coef_
    s['magnitude'] = np.abs(s['coef'])*scaler.std_
    print s.sort('magnitude',ascending=False).head(20)
    print "alpha ",clf.alpha_
    print "lambda ",clf.lambda_
    print "train r2 ",clf.score(X,y)
    print "val r2   ", r2_score(yval,clf.predict(Xval))
    print "trainerr/valerr ", np.sum((clf.predict(X)-y)**2)/len(y)/2/(np.sum((clf.predict(Xval)-yval)**2)/len(yval)/2)
    print clf.predict(X)
    for yr in range(2005,2080,5):
        print yr, np.sum(clf.predict(scaler.transform(_X[fullprep[YEAR]==yr][fullprep[SSP]=='SSP2']))*fullprep[fullprep[YEAR]==yr][fullprep[SSP]=='SSP2'][GDP])
    '''
    print "2005 OBS", np.sum(np.exp(clf.predict(Xo2005)))
    print "2005 ", np.sum(np.exp(clf.predict(X2005)))
    print "2010 ", np.sum(np.exp(clf.predict(X2010)))
    print "2020 ", np.sum(np.exp(clf.predict(X2020)))
    print "2030 ", np.sum(np.exp(clf.predict(X2030)))
    print "2040 ", np.sum(np.exp(clf.predict(X2040)))
    print "2050 ", np.sum(np.exp(clf.predict(X2050)))
    print "2060 ", np.sum(np.exp(clf.predict(X2060)))
    print "2070 ", np.sum(np.exp(clf.predict(X2070)))
    print "2080 ", np.sum(np.exp(clf.predict(X2080)))
    '''
