import numpy as np
from observables import calculate_observables
from data import load_magnetic_field, build_random_electron_density, magnetic_file_names
from plot import plot_obs
from analysis import analyze_step

import param as p

def main():
    
    if p.single_file is None:
        file_names = magnetic_file_names(p.low_mach, p.data_path)
    else: 
        file_names = [p.data_path + p.single_file]
    
    
    obs = [None, None, None, None]
    calc_obs = [p.do_rm, p.do_i, p.do_qu, p.do_qu]
    
    stat_dict = None
    
    for i, fn in enumerate(file_names):
        print("Calculating observables for file {}".format(fn))
        
        if p.direction is None: 
            directions = [0, 1, 2]
        else: 
            directions = [p.direction]
        for direction in directions:
            if p.direction is None:
                print("Calculating observables for direction {}".format(direction))
            Bpar, Bperp, polang = load_magnetic_field(fn, p.gaussian, direction, p.do_qu + p.faraday_rotate)
            
            shp = list(Bpar.shape)
            del shp[direction]
            shp = tuple(shp)
            
            if i == 0:
                obs = [np.zeros(shp, dtype=float) if calc_obs[j] else None for j in range(4)]
            
            n_th = None
            n_cr = None
            
            if p.do_rm or p.faraday_rotate:
                if p.th_random:
                    n_th = build_random_electron_density(Bpar.shape, **p.th_random_params) # type: ignore
                else:
                    n_th = p.th_n0
                
        
            if p.do_i or p.do_qu:
                if p.cr_random:
                    n_cr = build_random_electron_density(Bpar.shape, **p.cr_random_params) # type: ignore
                else:
                    n_cr = p.cr_n0
                
            rm_prev = obs[0] if p.faraday_rotate else None
            
            _obs = calculate_observables(Bpar, Bperp, polang, n_th, n_cr, p.do_rm, p.do_i, p.do_qu, p.faraday_rotate, spectral_index=p.spectral_index, lambda_square=p.lambda_square, direction=direction, rm_prev = rm_prev)
            
            for j in range(4):
                if calc_obs[j]:
                    obs[j] += _obs[j]
            
            stat_dict = analyze_step(*obs, stat_dict)        
            
            del Bpar, Bperp, polang # avoid memory leaks
    
    n_boxes = len(file_names)*len(directions)
    plot_obs(*obs, stat_dict, n_boxes, p.plot_path, p.plot_name)
        
if __name__ == "__main__":
    main()