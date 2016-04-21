import numpy as np

def aggregate_scores(X, w):
    """
    INPUTS:
    indicator_values -- an mxn matrix where n is the number of indicators and m is the number of entries
    weights -- an 1xn vector of indicator weights
    null_value -- value that represents null
    
    OUTPUT:
    s -- a 1xm vector of entry scores
    
    Calculates a weighted average of indicators for each entry then re-scales to extend from
    highest possible weighted score to lowest possible weighted score
    
    Intermediate variables
    [m,n] = size(X)                        %-- count of features and indicators in A
    nans = isnan(X)                        %-- mxn matrix identifying where features' indicators are null
    Ws = repmat(w,m,1); Ws(nans)=0         %-- mxn matrix weights for each feature with null values zeroed out
    sumWs = sum(Ws,2)                      %-- mx1 vector sum of weights for each feature
    zX = X; zX(nans)=0                     %-- mxn matrix of indicator values with null zeroed out
    a = (zX*w')./sumWs                     %-- mx1 vector of weighted averages
    mina = min(a)                          %-- lowest score
    maxa = max(a)                          %-- highest score
    s = (a-mina)/(maxa-mina)*5
    
    If low and high values are not guarenteed:
    nani = sum(~nans,1)==0                 %-- 1xn vector identifying all-null indicators
    mini = min(X,[],1); mini(nani)=0       %-- 1xn vector lowest value for each indicator; null zeroed out
    maxi = max(X,[],1); maxi(nani)=0       %-- 1xn vector highest value for each indicator; null zeroed out
    sumw = sum(w(~nani))                   %-- sum of weights with all-null indicators ignored
    nmin = sum(mini.*w)/sumw               %-- weighted min of all indicators (new lowest score)
    nmax = sum(maxi.*w)/sumw               %-- weighted max of all indicators (new highest score)
    s = ((a-mina)/(maxa-mina)*(nmax-nmin)+nmin)
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
    
    #    zX = X; zX(nans)=0                     %-- mxn matrix of indicator values with null zeroed out
    X[nans] = 0
    
    #    a = (zX*w')./sumWs                     %-- mx1 vector of weighted averages
    a = (X*w.T)
    a = a/sumWs
    
    #    mina = min(a)                          %-- lowest score
    mina = np.nanmin(a)
    #    maxa = max(a)                          %-- highest score
    maxa = np.nanmax(a)
    
    #    nani = sum(~nans,1)==0                 %-- 1xn vector identifying all-null indicators
    #    mini = min(X,[],1); mini(nani)=0       %-- 1xn vector lowest value for each indicator; null zeroed out
    #    maxi = max(X,[],1); maxi(nani)=0       %-- 1xn vector highest value for each indicator; null zeroed out
    #    sumw = sum(w(~nani))                   %-- sum of weights with all-null indicators ignored
    #    nmin = sum(mini.*w)/sumw               %-- weighted min of all indicators (new lowest score)
    #    nmax = sum(maxi.*w)/sumw               %-- weighted max of all indicators (new highest score)
    
    #    s = ((a-mina)/(maxa-mina)*(nmax-nmin)+nmin)
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

