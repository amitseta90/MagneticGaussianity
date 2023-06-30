import matplotlib.pyplot as pl
import cmasher as cm


def plot_obs(rm, i, q, u, do_lic=False, path='./Plot/'):
    
    fields = [rm, i, q, u]
    do_field = [not f is None for f in fields]
    
    if do_field[2] + do_field[3] == 1:
        raise ValueError('Thats odd, either both q and u should be given or None of them')
    
    if not do_lic:
        cmaps = ['prinsenvlag_r', 'viridis', 'magma', 'magma']
        names = ['RM', 'I', 'Q', 'U']
    else:
        cmaps = ['prinsenvlag_r', 'viridis', 'magma', 'magma']
        

    
    n_plots = sum(do_field)
    
    if n_plots == 1:
        fig, ax  = pl.subplots(ncols=1, nrows=1)
        map(fields.__delitem__, sorted(do_field, reverse=True))
        ax.imshow(fields[0], 
                  # cmap=[cmaps[do_field]]
                  )
        
        fig.savefig(path + 'rm', dpi=200)
        
    elif n_plots == 2:
    
        fig, ax  = pl.subplots(ncols=2, nrows=1) 
    