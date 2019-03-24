import numpy as np
import pylops

def deriv(D,dx):    
    
    fre = np.fft.fft2(D)
    kn=1/(2*dx)
    ks = np.fft.fftfreq(nr, d=dx)

    coeff1 = 1j*2*np.pi*ks
    coeff2 = -(2*np.pi*ks)**2

    coeff1_m = np.tile(coeff1,nt)
    coeff2_m = np.tile(coeff2,nt)

    D1op_hand = pylops.Diagonal(coeff1_m)
    D2op_hand = pylops.Diagonal(coeff2_m)

    D1_hand_fre = D1op_hand*fre.flatten()
    D2_hand_fre = D2op_hand*fre.flatten()

    D1_hand = F.H*D1_hand_fre
    D2_hand = F.H*D2_hand_fre

    return D1_hand, D2_hand, D1op_hand, D2op_hand