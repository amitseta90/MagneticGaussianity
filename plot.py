import matplotlib.pyplot as pl
from matplotlib import cm
import cmasher as cma
import numpy as np



def get_cmap(cm_string):
    if cm_string == '':
        return None
    try:
        cmap = getattr(cm, cm_string)
        return cmap
    except AttributeError:
        cmap = getattr(cma, cm_string)
        return cmap


def plot_obs(rm, i, q, u, path='./Plot/'):
    
    fields = [rm, i, q, u]
    do_field = [not f is None for f in fields]
    
    if do_field[2] + do_field[3] == 1:
        raise ValueError('Thats odd, either both q and u should be given or None of them')
    
    cmaps = ['prinsenvlag_r', 'viridis', 'magma', 'magma']
    names = ['RM', 'I', 'Q', 'U']

    n_plots = sum(do_field)
    
    map(fields.__delitem__, sorted(do_field, reverse=True))
    map(names.__delitem__, sorted(do_field, reverse=True))
    map(cmaps.__delitem__, sorted(do_field, reverse=True))
    
    if n_plots == 1:
        fig, ax  = pl.subplots(ncols=1, nrows=1)
        map(fields.__delitem__, sorted(do_field, reverse=True))
        ax.imshow(fields[0], 
                  cmap=get_cmap(cmaps[0]), 
                  title=names[0]
                  )
        mappable = ax.get_images()[0]
        fig.colorbar(mappable, ax=ax)
        
        
        fig.savefig(path + names[0], dpi=200)
        
    elif n_plots == 2:
    
        fig, ax  = pl.subplots(ncols=2, nrows=1) 
        ax[0].imshow(fields[0], 
                  cmap=get_cmap(cmaps[0])
                  )
        mappable = ax[0].get_images()[0]
        fig.colorbar(mappable, ax=ax[0])
        
        ax[1].imshow(fields[1], 
                  cmap=get_cmap(cmaps[1])
                  )
        mappable = ax[1].get_images()[0]
        fig.colorbar(mappable, ax=ax[1])
        pl.tight_layout()
        fig.savefig(path + names[0] + '_' + names[1], dpi=200)
        
    else: 
        
        fig, ax  = pl.subplots(ncols=2, nrows=2) 
        
        pos = [(0, 0), (0, 1), (1, 0), (1, 1), ]
        
        for i in range(n_plots):
            
            j, k = pos[i] 
            (ax[j][k]).imshow(fields[i], 
                    cmap=get_cmap(cmaps[i])
                    )
            mappable = ax[j, k].get_images()[0]
            fig.colorbar(mappable, ax=ax[j, k])
        fig.savefig(path + 'all_obs', dpi=200)
    