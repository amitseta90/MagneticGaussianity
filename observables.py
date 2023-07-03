import numpy as np 


def calculate_observables(B_par, B_perp,  pol_angle, n_th, n_cr, do_rm=False, do_syncI = False, do_syncQU= False, faraday_rotate=False, spectral_index = 3., lambda_square=1., direction=0, rm_prev=None):
    
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
    
    shape = None
    for f in (B_perp, B_par, n_cr, n_th): 
        if isinstance(f, np.ndarray):
            if shape is None:
                shape = f.shape
            else: 
                if shape != f.shape: # type: ignore
                    raise ValueError("Inconsistent shapes")
        elif not (isinstance(f, float) or f is None):
            raise TypeError("Fields must be numpy arrays or a single float, {} detected".format(type(f))) 
             
    if shape is None:
        raise ValueError("At last one np.ndarray must be provided")
    
    lsd = None
    
    if do_rm or faraday_rotate: 
        fs = B_par*n_th
        if faraday_rotate: 
            lsd = faraday_depth(fs, direction, rm_prev)  
            if do_rm: 
                slc = [slice(None), slice(None), slice(None)]
                slc[direction] = -1
                results[0] = lsd[tuple(slc)]
            lsd *= lambda_square
        else:
            if do_rm:
                results[0] = np.sum(fs, axis=direction)

    if do_syncI or do_syncQU:
        si, sq, su = synchrotron_emissivities(B_perp, n_cr, pol_angle, spectral_index, lsd) 
        if do_syncI:
            results[1] = np.sum(si, axis=direction)
        if do_syncQU:
            results[2] = np.sum(sq, axis=direction)
            results[3] = np.sum(su, axis=direction)
            
    return tuple(results)
    

def synchrotron_emissivities(B_perp, n_cr, pol_angle=False, spectral_index=3., lambda_square_fd=None):
    
    s_i = B_perp**((spectral_index + 1)/2)*n_cr

    if pol_angle is not None:
        rel_factor = (spectral_index + 1)/(spectral_index + 7./3) # type: ignore
        if lambda_square_fd is not None:
            pol_angle += lambda_square_fd
        s_q = s_i*rel_factor*np.cos(2*pol_angle) 
        s_u = s_i*rel_factor*np.sin(2*pol_angle) 
    else:
        s_q = None
        s_u = None    
    return (s_i, s_q, s_u)


def faraday_depth(fs, direction, prev_rm):
    dr = 1.
    fd = np.cumsum(np.concatenate((np.expand_dims(prev_rm, direction), fs*dr), axis=direction), axis=direction)
    fd = np.delete(fd, 0, direction)
    return fd
    
    
    