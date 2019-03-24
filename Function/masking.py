import numpy as np
import pylops
# mask for direct waves

def mask_time(D,shot,dt,dx,vel):
    # setup
    # dt = 4e-3
    # dx = 10
    # vel_ocean = 1490
    nt,nr = D.size
    shot = shot - 1     # python stuffs start with zero

    x1 = np.arange(shot)
    x2 = np.arange(shot,nr)
    t1 = (shot-x1)*dx/(vel*dt)
    t2 = (x2-shot)*dx/(vel*dt) 
    t_vec = np.concatenate((t1,t2),axis=None) + 140

    # mask for sediment reflection
    t3 = np.sqrt(830**2 + ((shot-x1)*dx)**2/((vel*dt)**2))
    t4 = np.sqrt(830**2 + ((x2-shot)*dx)**2/((vel*dt)**2))
    t_vec2 = np.concatenate((t3,t4),axis=None)

    mask_t2 = np.zeros((nt,nr))
    for i in np.arange(nr):
        mask_t2[int(t_vec[i]):int(t_vec2[i]),i] = 1

    Sop_t = pylops.Smoothing2D(nsmooth=[11,3], dims=[nt, nr])

    mask_2 = pylops.Diagonal(Sop_t*mask_t2.flatten())
    D_mask = (mask_2*D.flatten()).reshape(nt,nr)

    return D_mask,mask_2


def mask_fre(D,shot,dt,dx,vel): 
    """

    Under construction, need to pratice on different data 
    with different shot locations

    """

    kn=1/(2*dx)
    dk=2*kn/nr

    mask_fre_loc = np.zeros((nt,nr))

    v = np.zeros(nt)
    k1 = np.zeros(nt)
    k2 = np.zeros(nt)
    for i in np.arange(350,540):
    #     v[i] = -vn + i*dv
        k1[i] = ((-vn + i*dv)/(vel)) /dk +shot
        k2[i] = ((-vn + i*dv)/(-1*vel)) /dk +shot
        mask_fre_loc[i,int(k1[i]):int(k2[i])] = 1
    for i in np.arange(540,730):
        k1[i] = ((-vn + i*dv)/(vel) ) /dk +shot
        k2[i] = ((-vn + i*dv)/(-1*vel) ) /dk +shot
        mask_fre_loc[i,int(k2[i]):int(k1[i])] = 1

    mask_fre_loc[530:550,140:160] = 1
    mask_fre_iff = np.fft.ifftshift(mask_fre_loc.reshape(nt,nr))
    mask_fre = pylops.Diagonal(mask_fre_iff)
    fre_dec = np.fft.fftshift(np.fft.fft2(D_dec_mask))    

    return mask_fre