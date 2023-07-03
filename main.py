import numpy as np
from observables import calculate_observables
from data import load_magnetic_field, build_random_electron_density, magnetic_file_names
from plot import plot_obs

import param as p

def main():
    
    if p.single_file is None:
        file_names = magnetic_file_names(p.low_mach, p.data_path)
    else: 
        file_names = [p.data_path + p.single_file]
    
    
    obs = [None, None, None, None]
    calc_obs = [p.do_rm, p.do_i, p.do_qu, p.do_qu]
    
    for i, fn in enumerate(file_names):
        print("Calculating observables for file {}".format(fn))
        Bpar, Bperp, polang = load_magnetic_field(fn, p.gaussian, p.direction, p.do_qu + p.faraday_rotate)
        
        shp = list(Bpar.shape)
        del shp[p.direction]
        shp = tuple(shp)
        
        if i == 0:
            obs = [np.zeros(shp, dtype=float) if calc_obs[j] else None for j in range(4)]
        
        n_th = None
        n_cr = None
        
        if p.do_rm or p.faraday_rotate:
            if p.th_random:
                # params = {key: p.th_random_params[key] for key in p.th_random_params}
                n_th = build_random_electron_density(Bpar.shape, **p.th_random_params) # type: ignore
            else:
                n_th = p.th_n0
            
    
        if p.do_i or p.do_qu:
            if p.cr_random:
                # params = {key: config["cr_random_params"].getfloat(key) for key in config["cr_random_params"]}
                n_cr = build_random_electron_density(Bpar.shape, **p.cr_random_params) # type: ignore
            else:
                n_cr = p.cr_n0
            
    
        _obs = calculate_observables(Bpar, Bperp, polang, n_th, n_cr, p.do_rm, p.do_i, p.do_qu, p.faraday_rotate, spectral_index=p.spectral_index, lambda_square=p.lambda_square, direction=p.direction, rm_prev = obs[0])
        
        for j in range(4):
            if calc_obs[j]:
                obs[j] += _obs[j]
    
    plot_obs(*obs, p.plot_path)
        
if __name__ == "__main__":
    main()