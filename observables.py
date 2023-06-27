import numpy as np 
from scipy.special import gamma



def synchrotron(integrator, B_perp, n_cr, spectral_index, observing_frequency, return_q_and_u=False, fd=None):
    
    s_i = None
    s_q = None 
    s_u = None

    if return_q_and_u:
        r, phi, theta = spherical cooridnates
        rel_factor = (gamma(spectral_index/4 + 7./12)*4)/(gamma(spectral_index/4 + 19./12)*(spectral_index - 1))
        s_q = None 
        s_u = None
        if fd is not None:
            s_q =  s_q*sin(2 ) - 
            
    
    
    return (s_i, s_q, s_u)


def _calc_pol_angle


def faraday(B, n_th):
    return
    