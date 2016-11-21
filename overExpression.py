import scipy.stats as st

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
