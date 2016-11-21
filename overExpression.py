import scipy.stats as st
import numpy as np
from multiprocessing import Pool
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
    
def SVN(mat,tres):
    N = mat.shape[0]
    A,B = np.triu_indices(N,k=1)
    X = zip(A,B)
    A = mat[X]
    p = Pool(processes=16)
    D = zip(X, p.map(pvalues, A,16))
    D = sorted(D,key=lambda x : x[1])
    P = np.array(zip(*D)[1])
    K = 2*tres/(N*(N-1)) * np.arange(1,len(P)+1)
    i = np.where(P<K)[0]
    edges = list(np.array(zip(*D)[0])[i])
    g = igraph.Graph(N,edges)
    return g,edges
