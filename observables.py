import numpy as np 
import scipy.special as sp


def synchrotron_emissivities(B_perp, n_cr, spectral_index, pol_angle=False, lambda_square_fd_r=None):
    
    s_i = B_perp**()*n_cr

    if pol_angle is not None:
        rel_factor = (sp.gamma(spectral_index/4 + 7./12)*4)/(sp.gamma(spectral_index/4 + 19./12)*(spectral_index - 1)) # type: ignore
        s_q = s_i*rel_factor*np.cos(2*pol_angle) 
        s_u = s_i*rel_factor*np.sin(2*pol_angle) 
        if lambda_square_fd_r is not None:
            s_q, s_u = _rotate_q_and_u(s_q, s_u, lambda_square_fd_r)
    else:
        s_q = None
        s_u = None    
    return (s_i, s_q, s_u)
    

def faraday_depth(B_par, n_th):
    return B_par*n_th


def _rotate_q_and_u(q, u , l2_fd_r):
    _q =  q*np.sin(2*l2_fd_r) - u*np.cos(2*l2_fd_r)
    _u =  q*np.cos(2*l2_fd_r) + u*np.sin(2*l2_fd_r)
    return _q, _u
    