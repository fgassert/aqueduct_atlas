'''
Created on Nov 27, 2012

@author: Francis Gassert

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/3.0/.
'''

import numpy as np

def aggregate_scores(X, w):
    """
    INPUTS:
    X -- an mxn matrix where n is the number of indicators and m is the number of entries
    w -- an 1xn vector of indicator weights
    
    OUTPUT:
    s -- a 1xm vector of entry scores
    
    Calculates a weighted average of indicators for each entry then re-scales to extend from 0 to 5
    Ignores null values
    
    Intermediate variables
    [m,n] = size(X)                        %-- count of features and indicators in A
    nans = isnan(X)                        %-- mxn matrix identifying where features' indicators are null
    Ws = repmat(w,m,1); Ws(nans)=0         %-- mxn matrix weights for each feature with null values zeroed out
    sumWs = sum(Ws,2)                      %-- mx1 vector sum of weights for each feature
    X(nans)=0                              %-- mxn matrix of indicator values with null zeroed out
    a = (X*w')./sumWs                      %-- mx1 vector of weighted averages
    mina = min(a)                          %-- lowest score
    maxa = max(a)                          %-- highest score
    s = (a-mina)/(maxa-mina)*5
    """
    
    #   ensure matrix operation
    w = np.matrix(w, dtype=np.double)
    X = np.matrix(X, dtype=np.double)
    
    #    [m,n] = size(X)                        %-- count of features and indicators in A
    m,n = X.shape
    
    #    nans = isnan(X)                        %-- mxn matrix identifying where features' indicators are null
    nans = np.isnan(X)
    
    #    Ws = repmat(w,m,1); Ws(nans)=0         %-- mxn matrix weights for each feature with null values zeroed out
    Ws = np.repeat(w,m,0)
    Ws[nans] = 0
    
    #    sumWs = sum(Ws,2)                      %-- mx1 vector sum of weights for each feature
    sumWs = np.sum(Ws,1)
    
    #    X(nans)=0                              %-- mxn matrix of indicator values with null zeroed out
    X[nans] = 0
    
    #    a = (X*w')./sumWs                      %-- mx1 vector of weighted averages
    a = (X*w.T)
    a = a/sumWs
    
    #    mina = min(a)                          %-- lowest score
    mina = np.nanmin(a)
    #    maxa = max(a)                          %-- highest score
    maxa = np.nanmax(a)
    
    #    s = (a-mina)/(maxa-mina)*5
    s = (a-mina)/(maxa-mina)*5
            
    return s

#
if __name__ == "__main__":
    obs1 = [None,None,None]
    obs2 = [3,4,None]
    obs3 = [0,5,None]
    obs4 = [5,0,None]
    obs5 = [4,None,None]
    obs = [obs1,obs2,obs3,obs4,obs5]
    weights = [4,8,4]
    null_value = None
    scores = aggregate_scores(obs, weights)
    print scores

