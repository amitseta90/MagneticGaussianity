import numpy as np
import nifty8 as ift
import h5py as h5



def load_magnetic_field(name, gaussian, path='./Data/'):
    with h5.File(path + name, "r") as f:
        if gaussian:
            bx = f['bxG']
            by = f['byG']
            bz = f['bzG']
        else:
            bx = f['bxNG']
            by = f['byNG']
            bz = f['bzNG']           
    return (bx, by, bz)


def build_random_electron_density(shape, offset_mean, offset_std, fluctuations, loglogavgslope, flexibility=None, asperity=None):
    domain = ift.makeDomain(ift.RGSpace(shape))
    f = ift.SimpleCorrelatedField(domain, offset_mean, offset_std, fluctuations, loglogavgslope, flexibility, asperity)    
    return f(ift.from_random(f.domain)).val_rw()

