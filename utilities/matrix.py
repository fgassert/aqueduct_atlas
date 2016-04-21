import numpy as np

#f = open(r"C:\Users\francis.gassert\Documents\mailinglists_nodes_noname.csv","rb")
a = np.loadtxt(r"C:\Users\francis.gassert\Documents\mailinglists_nodes_noname.csv",delimiter=",",skiprows=1)
b = np.transpose(a)

c = np.dot(a,b)
d = np.dot(b,a)

m = c.shape[0]
n = c.shape[1]
col1=np.arange(m*n)%m
col2=np.floor(np.arange(m*n)/m).astype('i4')
col3=c[col1,col2]

c2 = np.column_stack((col1,col2,col3))
c3 = c2[col3>0,:]

np.savetxt("a_dot_aT.csv",c3,delimiter=',')

m = d.shape[0]
n = d.shape[1]
col1=np.arange(m*n)%m
col2=np.floor(np.arange(m*n)/m).astype('i4')
col3=d[col1,col2]

d2 = np.column_stack((col1,col2,col3))
d3 = d2[col3>0,:]

np.savetxt("aT_dot_a.csv",d3,delimiter=',')