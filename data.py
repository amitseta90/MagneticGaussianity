import numpy as np
import nifty8 as ift
import h5py as h5
import glob


def simulation_file_names(low_mach, path='./Data/'):
    if low_mach: 
        files = glob.glob(path + "sm0p1*.h5")
    else:
        files = glob.glob(path + "sm10*.h5")
    return files
    
def bpol_from_perp(bperp_1, bperp_2, return_polang):
    b_perp = np.sqrt(bperp_1**2 + bperp_2**2)
    polang = None

    if return_polang:
        polang = 0.5*np.arctan2(bperp_2,  bperp_1) + np.pi/2 # + pi/2, since sync radiation is perpendicular to magnetic field direction
    
    return (b_perp, polang)

    
def load_electron_density(path):
    with h5.File(path, "r") as f:
        nth = f['ne' ][: ,: ,:] # type: ignore
    return nth


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
        
        b_perp, polang = bpol_from_perp(f[b_perp_x_key][: ,: ,:], f[b_perp_y_key][: ,: ,:], return_polang)
        
    return (bpar, b_perp, polang)


def build_random_electron_density(shape, offset_mean, offset_std, fluctuations, loglogavgslope,  flexibility=None, asperity=None):
    domain = ift.makeDomain(ift.RGSpace(shape))
    f = ift.SimpleCorrelatedField(domain, offset_mean=offset_mean, offset_std=offset_std, fluctuations=fluctuations, flexibility=flexibility, asperity=asperity, loglogavgslope=loglogavgslope)    
    return f(ift.from_random(f.domain)).val_rw()

