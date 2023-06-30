import numpy as np 
import scipy.special as sp
import nifty8 as ift

def cartesian(shape, direction):
    domain = ift.makeDomain(ift.RGSpace(shape))
    return ift.IntegrationOperator(domain, spaces=direction)


def calculate_observables(B_perp, B_par, pol_angle, n_th, n_cr, do_rm=False, do_syncI = False, do_syncQU= False, faraday_rotate=False, spectral_index = 3., lambda_square=1., direction=0):
    
    if not do_rm and not do_syncI and not do_syncQU:
        raise ValueError("Nothing to do")
    
    if do_rm or faraday_rotate:
        if B_par is None:
            raise ValueError
        if n_th is None: 
            raise ValueError
    
    if do_syncI or do_syncQU:
        if B_perp is None:
            raise ValueError
        if n_cr is None: 
            raise ValueError
    
    results = [None, None, None, None] # RM, I, Q, U
    
    domain = None
    for f in (B_perp, B_par, n_cr, n_th): 
        if isinstance(f, np.ndarray):
            if domain is None:
                domain = ift.makeDomain(ift.RGSpace(f.shape))
            else: 
                if domain.shape != f.shape: # type: ignore
                    raise ValueError("Inconsistent shapes")
        elif not (isinstance(f, float) or f is None):
            raise TypeError("Fields must be numpy arrays or a single float, {} detected".format(type(f))) 
             
    if domain is None:
        raise ValueError("At last one np.ndarray must be provided")
    

    integrator = cartesian(domain.shape, direction) # type: ignore
    
    lsd = None
    
    if do_rm or faraday_rotate: 
        fs = faraday_source(B_par, n_th)
        if do_rm:
            results[0] = integrator(ift.makeField(domain, fs)).val
        if faraday_rotate: 
            lsd = lambda_square*faraday_depth(fs, direction)  

    if do_syncI or do_syncQU:
        si, sq, su = synchrotron_emissivities(B_perp, n_cr, pol_angle, spectral_index, lsd) 
        if do_syncI:
            results[1] = integrator(si).val
        if do_syncQU:
            results[2] = integrator(sq).val
            results[3] = integrator(su).val
            
    return tuple(results)
    

def synchrotron_emissivities(B_perp, n_cr, pol_angle=False, spectral_index=3., lambda_square_fd=None):
    
    s_i = B_perp**((spectral_index + 1)/2)*n_cr

    if pol_angle is not None:
        rel_factor = (sp.gamma(spectral_index/4 + 7./12)*4)/(sp.gamma(spectral_index/4 + 19./12)*(spectral_index - 1)) # type: ignore
        if lambda_square_fd is not None:
            pol_angle += lambda_square_fd
        s_q = s_i*rel_factor*np.cos(2*pol_angle) 
        s_u = s_i*rel_factor*np.sin(2*pol_angle) 
    else:
        s_q = None
        s_u = None    
    return (s_i, s_q, s_u)


def faraday_source(B_par, n_th):
    return B_par*n_th
    

def faraday_depth(fs, direction):
    dr = 1.
    return np.cumsum(fs*dr, axis=direction)
    
    
    