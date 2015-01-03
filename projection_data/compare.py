
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

incsv = 'csvs/use_comparison.csv'

a = pd.read_csv(incsv)
a.fillna(0,inplace=True)

linx = np.arange(4)*10.0

ax = plt.subplot(131)
x = a['CT_GLDAS']/1.0e9
y = a['RCP85_SSP3']/1.0e9
#y = y[x<30]
#x = x[x<30]
l = lowess(y,x,frac=.05)

plt.plot(x,y,'.',color='blue',alpha =.25)
plt.plot(linx,linx,'--',lw=1,color='black')
plt.plot(l[:,0],l[:,1],'-',lw=1,color='red')
plt.xlabel('Gassert et al. (2014)')
plt.ylabel('This study')
plt.xticks([10.0,20.0,30.0])
plt.yticks([10.0,20.0,30.0])

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

ax = plt.subplot(132)
x = a['GLOWASIS']/1.0e9
y = a['RCP85_SSP3']/1.0e9
l = lowess(y,x,frac=.05)

plt.plot(x,y,'.',color='blue',alpha=.25)
plt.plot(linx,linx,'--',lw=1,color='black')
plt.plot(l[:,0],l[:,1],'-',lw=1,color='red')
plt.xlabel('Wada et al. (2011, 2012)')
plt.ylabel('This study')
plt.xticks([10.0,20.0,30.0])
plt.yticks([10.0,20.0,30.0])

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


ax = plt.subplot(133)
x = a['Hoekstra']/1.0e9
y = a['RCP85_SSP3']/1.0e9
l = lowess(y,x,frac=.05)

plt.plot(x,y,'.',color='blue',alpha=.25)
plt.plot(linx,linx,'--',lw=1,color='black')
plt.plot(l[:,0],l[:,1],'-',lw=1,color='red')
plt.xlabel('Mekonnen and Hoekstra (2011)')
plt.ylabel('This study')
plt.xticks([10.0,20.0,30.0])
plt.yticks([10.0,20.0,30.0])

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


plt.show()
