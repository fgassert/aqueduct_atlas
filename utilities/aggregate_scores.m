function s = aggregate_scores(X, w)
%   INPUTS:
%   X -- an m,n matrix of indicator values 
%        where n is the number of indicators and m is the number of features
%   w -- an 1xn vector of indicator weights
%   
%   OUTPUT:
%   s -- a 1xm vector of feature scores
%   
%   Calculates a weighted average of indicators for each feature then re-scales to extend from
%   highest possible weighted score to lowest possible weighted score
%   
%   
%
%   Intermediate variables
%   [m,n] = size(X)                        %-- count of features and indicators in A
%   nans = isnan(X)                        %-- mxn matrix identifying where features' indicators are null
%   Ws = repmat(w,m,1); Ws(nans)=0         %-- mxn matrix weights for each feature with null values zeroed out
%   sumWs = sum(Ws,2)                      %-- mx1 vector sum of weights for each feature
%   zX = X; zX(nans)=0                     %-- mxn matrix of indicator values with null zeroed out
%   a = (zX*w')./sumWs                     %-- mx1 vector of weighted averages
%   mina = min(a)                          %-- lowest score
%   maxa = max(a)                          %-- highest score
%   nani = sum(~nans,1)==0                 %-- 1xn vector identifying all-null indicators
%   mini = min(X,[],1); mini(nani)=0       %-- 1xn vector lowest value for each indicator; null zeroed out
%   maxi = max(X,[],1); maxi(nani)=0       %-- 1xn vector highest value for each indicator; null zeroed out
%   sumw = sum(w(~nani))                   %-- sum of weights with all-null indicators ignored
%   nmin = sum(mini.*w)/sumw               %-- weighted min of all indicators (new lowest score)
%   nmax = sum(maxi.*w)/sumw               %-- weighted max of all indicators (new highest score)
%   s = ((a-mina)/(maxa-mina)*(nmax-nmin)+nmin) 
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    [m,n] = size(X);
    % initialize s to nulls
    s = NaN(m,1);
    % make sure at least one indicator is weighted, else return all nulls
    if sum(w) <= 0
        return;
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % find null indicator values
    nans = isnan(X);
    % duplicate weights for each feature and set weight to zero where the indicator is null
    Ws = repmat(w,m,1);
    Ws(nans) = 0;
    % sum weights for each feature
    sumWs = sum(Ws,2);
    % calculate sum of weights for each feature for normalization
    % duplicate indicator values and set nulls to zero
    zX = X;
    zX(nans) = 0;
    % generate weighted averages a for each feature; 0/0 -> NaN
    a = (zX*w')./sumWs;
    % calculate min and max for normalization
    mina = min(a);
    maxa = max(a);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % if a is all null, return
    if isnan(mina)
        return;
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % This section can be skipped when we know the maximum
    % and minimum values for each indicator extend from 0-5
    % In which case, nmin = 0 and nmax = 5
    
    % identify all-null indicators
    nani = sum(~nans,1)==0;
    % calculate mini and maxi as minimum and maximum scores for each indicator with null indicators zeroed out
    mini = min(X,[],1); mini(nani)=0;
    maxi = max(zX,[],1);
    % calculate sum of weights ignoring all-null indicators
    sumw = sum(w(~nani));
    % calculate nmin and nmax as new minimum and maximum
    nmin = mini*w'/sumw;
    nmax = maxi*w'/sumw;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % calculate final rescaled scores
    s = ((a - mina)/(maxa - mina)*(nmax - nmin)+nmin);
    
end