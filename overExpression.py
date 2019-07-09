import scipy.stats as st
import numpy as np
from multiprocessing import Pool,cpu_count()
import igraph 

def oeHypergeom(N,N1,N2,N12,mode=['over','under','both']):
    if mode=='over':
      p1 = st.hypergeom.sf(N12-1,N,N1,N2)
      return [p1]
    elif mode=='under':
      p2 = st.hypergeom.cdf(N12,N,N1,N2) 
      return [p2]
    elif mode=='both':
      p1 = st.hypergeom.sf(N12-1,N,N1,N2)
      p2 = st.hypergeom.cdf(N12,N,N1,N2) 
      return [p1,p2]
    else:
      raise Exception('Mode is not valid')

def pHypergeom(a):
    x,y = a
    N = len(x)
    N1 = x.sum()
    N2 = y.sum()
    N12 = (x*y).sum()
    return st.hypergeom.sf(N12-1,N,N1,N2)

def projectMatBip(mat):
    A,B = np.where(mat==1)
    B = B + len(A)
    edges = zip(A,B)
    g = igraph.Graph.Bipartite([0]*len(A)+[1]*len(B),edges)
    g = g.bipartite_projection()[0]
    return g
    
def SVN(mat,tres):
    N = mat.shape[0]
    X = projectMatBip(mat).get_edgelist()
    A = mat[X]
    p = Pool(processes=cpu_count())
    D = zip(X, p.map(pHypergeom, A))
    D = sorted(D,key=lambda x : x[1])
    P = np.array(zip(*D)[1])
    K = 2*tres/(N*(N-1)) * np.arange(1,len(P)+1)
    i = np.where(P<K)[-1]
    edges = list(np.array(zip(*D)[0])[i])
    g = igraph.Graph(N,edges)
    return g
