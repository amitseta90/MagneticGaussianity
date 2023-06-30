import numpy as np
import nifty8 as ift
import h5py as h5
import glob


def magnetic_file_names(low_mach, path='./Data/'):
    if low_mach: 
        files = glob.glob(path + "sm0p1*.h5")
    else:
        files = glob.glob(path + "sm10*.h5")
    return files
    


def load_magnetic_field(path, gaussian, direction, return_polang):
    with h5.File(path, "r") as f:
        
        if direction == 0: 
            b_par_key = 'bxG' if gaussian else 'bxNG'
            b_perp_x_key = 'byG' if gaussian else 'byNG'
            b_perp_y_key = 'bzG' if gaussian else 'bzNG'
        elif direction == 1:
            b_par_key = 'byG' if gaussian else 'byNG'
            b_perp_x_key = 'bzG' if gaussian else 'bzNG'
            b_perp_y_key = 'bxG' if gaussian else 'bxNG'
        elif direction == 2:
            b_par_key = 'bzG' if gaussian else 'bzNG'
            b_perp_x_key = 'bxG' if gaussian else 'bxNG'
            b_perp_y_key = 'byG' if gaussian else 'byNG'
        else:
            raise ValueError
            
        bpar = f[b_par_key][: ,: ,:] # type: ignore
        
        b_perp = np.sqrt(f[b_perp_x_key][: ,: ,:]**2 + f[b_perp_y_key][: ,: ,:]**2) # type: ignore
        
        polang = None
        if return_polang:
            polang =np.arctan2(f[b_perp_y_key][: ,: ,:],  f[b_perp_x_key][: ,: ,:]) + np.pi/2 # type: ignore
             
    return (bpar, b_perp, polang)


def build_random_electron_density(shape, offset_mean, offset_std, fluctuations, loglogavgslope, flexibility=None, asperity=None):
    domain = ift.makeDomain(ift.RGSpace(shape))
    f = ift.SimpleCorrelatedField(domain, offset_mean, offset_std, fluctuations, loglogavgslope, flexibility, asperity)    
    return f(ift.from_random(f.domain)).val_rw()

