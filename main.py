import numpy as np
from observables import calculate_observables
from data import load_magnetic_field, build_random_electron_density, simulation_file_names, load_electron_density, bpol_from_perp
from plot import plot_obs, save_obs
from analysis import analyze_step

import param as p

def main():
    
    if p.single_file is None:
        file_names = simulation_file_names(p.low_mach, p.data_path)
    else: 
        file_names = [p.data_path + p.single_file]
    
    
    obs = [None, None, None, None]
    calc_obs = [p.do_rm, p.do_i, p.do_qu, p.do_qu]
    
    stat_dict = None
    
    if p.mag_type not in ["simulation", "constant"]:
        raise KeyError("mag_type in parameter file must be either 'simulation' or 'constant', but is {}".format(p.mag_type))
    
    if p.th_type not in ["random", "simulation", "constant"]:
        raise KeyError("th_type in parameter file must be either 'random', 'simulation' or 'constant', but is {}".format(p.th_type))
    
    if p.cr_type not in ["random", "constant"]:
        raise KeyError("cr_type in parameter file must be either 'random' or 'constant', but is {}".format(p.cr_type))
        
    shape = p.shape
    
    for i, fn in enumerate(file_names):
        print("Calculating observables for file {}".format(fn))
        
        
        n_th = None
        n_cr = None
        
        if p.do_rm or p.faraday_rotate:
            
            if p.th_type == "random":
                n_th = build_random_electron_density(shape, **p.th_random_params) # type: ignore
            elif p.th_type == "simulation":
                n_th = load_electron_density(fn) 
                shape = n_th.shape
            else:
                n_th = 1.
            n_th *= p.th_n0
            
        if p.do_i or p.do_qu:
            if p.cr_type == "random":
                n_cr = build_random_electron_density(shape, **p.cr_random_params) # type: ignore
            else:
                n_cr = 1. 
            n_cr *= p.th_n0
        
        if p.direction is None: 
            directions = [0, 1, 2]
        else: 
            directions = [p.direction]
        for direction in directions:
            if p.direction is None:
                print("Calculating observables for direction {}".format(direction))
            if p.mag_type == "simulation":
                Bpar, Bperp, polang = load_magnetic_field(fn, p.gaussian, direction, p.do_qu + p.faraday_rotate)
                shape = Bpar.shape
            else: 
                b = [p.bx, p.by, p.bz] 
                Bpar = b[direction]
                dir_1 = (direction + 1) % 3     
                dir_2 = (direction + 2) % 3     
                Bperp, polang = bpol_from_perp(b[dir_1], b[dir_2], p.do_qu + p.faraday_rotate)
            Bpar *= p.b_0
            Bperp *= p.b_0
                
            
            shp = list(shape)
            del shp[direction]
            shp = tuple(shp)
            
            if i == 0:
                obs = [np.zeros(shp, dtype=float) if calc_obs[j] else None for j in range(4)]
            
            rm_prev = obs[0] if p.faraday_rotate else None
            
            _obs = calculate_observables(Bpar, Bperp, polang, n_th, n_cr, p.do_rm, p.do_i, p.do_qu, p.faraday_rotate, spectral_index=p.spectral_index, lambda_square=p.lambda_square, direction=direction, rm_prev = rm_prev)
            
            for j in range(4):
                if calc_obs[j]:
                    obs[j] += _obs[j]
            
            stat_dict = analyze_step(*obs, stat_dict, do_pi=p.do_pi)        
            
            del Bpar, Bperp, polang # avoid memory leaks
    
    n_boxes = len(file_names)*len(directions)
    plot_obs(*obs, stat_dict, n_boxes, p.plot_path, p.name, p.save_pdfs, p.do_pi)
    save_obs(*obs, p.result_path, p.name, p.do_pi)
        
if __name__ == "__main__":
    main()