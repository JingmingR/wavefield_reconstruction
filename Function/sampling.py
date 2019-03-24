import numpy as np
import pylops

def re_sample(D,gap):
    nt,nr = D.size
    idr = np.arange(0,nr,gap)
    cod = np.arange(0,nt*nr).reshape(nt,nr)
    idx = cod[:,idr].flatten()
    R = pylops.Restriction(N, idx)
    D_dec = (R * D.flatten()).reshape(nt,idr.szie)
    D_adj = (R.H * D_dec).reshape(nt,nr)
    return D_dec, D_adj, idr.size

def irre_sample(D,gap):
    nt,nr = D.size
    interval = 6
    node = np.arange(0,nr,interval) 
    jitter = np.random.randint(interval,size=node.size-1)
    jitter_last = np.random.randint(nr - node[-1])
    jitter = np.concatenate((jitter,jitter_last),axis=None)
    idr = node + jitter

    cod = np.arange(0,nt*nr).reshape(nt,nr)
    idx = cod[:,idr].flatten()
    R = pylops.Restriction(N, idx)
    D_dec = (R * D.flatten()).reshape(nt,idr.szie)
    D_adj = (R.H * D_dec).reshape(nt,nr)
    return D_dec, D_adj, idr.size

def load_sample(D,file_name):
    idr = np.load('%s.npy' % file_name)
    cod = np.arange(0,nt*nr).reshape(nt,nr)
    idx = cod[:,idr].flatten()
    R = pylops.Restriction(N, idx)
    D_dec = (R * D.flatten()).reshape(nt,idr.szie)
    D_adj = (R.H * D_dec).reshape(nt,nr)
    return D_dec, D_adj, idr.size

def part_sample(D,s_min,s_max,gap_d,gap_s):
    # s_min = 44
    # s_max= 84

    # gap_d = 3
    # gap_s = 4
    node_s1 = np.arange(0,s_min,gap_s)
    node_s2 = np.arange(s_max,nr,gap_s)
    node_d = np.arange(s_min,s_max,gap_d)
    jitter_s1 = np.random.randint(gap_s,size=node_s1.size)
    jitter_s1[-1] = np.random.randint(s_min - node_s1[-1])
    jitter_s2 = np.random.randint(gap_s,size=node_s2.size)
    jitter_s2[-1] = np.random.randint(nr - node_s2[-1])
    jitter_d = np.random.randint(gap_d,size=node_d.size)
    jitter_d[-1] = np.random.randint(s_max - node_d[-1])

    jitter_d = 0    # regular sampling in the denser part
    # jitter_s1= 0
    # jitter_s2= 0

    idr = np.concatenate((node_s1+jitter_s1,node_d+jitter_d,node_s2+jitter_s2),axis=None)

    cod = np.arange(0,nt*nr).reshape(nt,nr)
    idx = cod[:,idr].flatten()

    R = pylops.Restriction(N, idx)
    D_dec = R*D_sqz
    D_adj = R.H*D_dec
    return D_dec, D_adj, idr.size