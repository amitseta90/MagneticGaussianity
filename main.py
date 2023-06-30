import configparser
import numpy as np
from observables import calculate_observables
from data import load_magnetic_field, build_random_electron_density, magnetic_file_names
from plot import plot_obs


def main():
    
    config = configparser.RawConfigParser()   
    config.read('param.cfg')
    
    
    
    obs = config['obs']
    
    do_rm = obs.getboolean("do_rm")
    do_i = obs.getboolean("do_syncI")
    do_qu = obs.getboolean("do_syncQU")
    fd_rot = obs.getboolean("faraday_rotate")
    direction = obs.getint("direction")
    
    gaussian = config["magnetic"].getboolean("gaussian")
    
    
    file_names = magnetic_file_names(config["magnetic"].getboolean("low_mach"))
    
    
    obs = [None, None, None, None]
    calc_obs = [do_rm, do_i, do_qu, do_qu]
    
    for i, fn in enumerate(file_names):
        Bpar, Bperp, polang = load_magnetic_field(fn, gaussian, direction, do_qu + fd_rot)
        
        shp = list(Bpar.shape)
        del shp[direction]
        shp = tuple(shp)
        
        if i == 0:
            obs = [np.zeros(shp, dtype=float) if calc_obs[j] else None for j in range(4)]
        
        n_th = None
        n_cr = None
        
        if do_rm or fd_rot:
            if config["th_electron"].getboolean("random"):
                params = {key: config["th_random_params"].getfloat(key) for key in config["th_random_params"]}
                n_th = build_random_electron_density(Bpar.shape, **params) # type: ignore
            else:
                n_th = config["th_electron"].getfloat("n0")
            
    
        if do_i or do_qu:
            if config["cr_electron"].getboolean("random"):
                params = {key: config["cr_random_params"].getfloat(key) for key in config["cr_random_params"]}
                n_cr = build_random_electron_density(Bpar.shape, **params) # type: ignore
            else:
                n_cr = config["cr_electron"].getfloat("n0")
            
    
        _obs = calculate_observables(Bpar, Bperp, polang, n_th, n_cr, do_rm, do_i, do_qu, fd_rot, spectral_index=config['physics'].getfloat('spectral_index'), lambda_square=config['physics'].getfloat('lambda_square'), direction=direction)
        
        for j in range(4):
            if calc_obs[j]:
                obs[j] += _obs[j]
    plot_obs(*obs, do_lic=False)
        
        #if 
        
if __name__ == "__main__":
    main()