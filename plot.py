import matplotlib.pyplot as pl
from matplotlib import cm
import numpy as np

def get_cmap(cm_string):
    if cm_string == '':
        return None
    cmap = getattr(cm, cm_string)
    return cmap


def plot_obs(rm, i, q, u, path='./Plot/', name='', save_pdfs=True):
    
    fields = [rm, i, q, u]
    do_field = [not f is None for f in fields]
    
    if do_field[2] + do_field[3] == 1:
        raise ValueError('Thats odd, either both q and u should be given or None of them')
    
    cmaps = ['RdBu_r', 'viridis', 'magma', 'magma']
    names = ['RM', 'I', 'Q', 'U']

    n_plots = sum(do_field)
    
    map(fields.__delitem__, sorted(do_field, reverse=True))
    map(names.__delitem__, sorted(do_field, reverse=True))
    map(cmaps.__delitem__, sorted(do_field, reverse=True))
    
    if n_plots == 1:
        fig, ax  = pl.subplots(ncols=1, nrows=1)
        ax.imshow(fields[0], 
                  cmap=get_cmap(cmaps[0]), 
                  )
        ax.set_title(names[0])
        mappable = ax.get_images()[0]
        fig.colorbar(mappable, ax=ax)
        
        pl_name = name + '_' + names[0]
        
        fig.savefig(path + pl_name + '_2d', dpi=200)
        
        pl.close('all')
        
        
        fig, ax  = pl.subplots(ncols=1, nrows=1)
        pdf, bins, _ = ax.hist(fields[0], bins=1000, density=True, histtype='step')
        ax.set_xlabel(names[0])
        ax.set_yscale('log')
        fig.savefig(path +  pl_name + '_hist', dpi=200)
        
        if save_pdfs:
            np.save(path + pl_name + '_ pdf.npy', pdf)
            np.save(path + pl_name + '_bins.npy', bins)
        pl.close('all')
        
    elif n_plots == 2:
    
        fig_im, ax_im  = pl.subplots(ncols=2, nrows=1) 
        fig_hist, ax_hist  = pl.subplots(ncols=2, nrows=1) 
        
        pl_name = names[0] + '_' + names[1] + '_' + name
        
        for i in range(n_plots):
        
            ax_im[i].imshow(fields[i], 
                  cmap=get_cmap(cmaps[i]), 
                )
            ax_im[i].set_title(names[i])
            mappable = ax_im[i].get_images()[0]
            fig_im.colorbar(mappable, ax=ax_im[i])
            
            pdf, bins, _ = ax_hist[i].hist(fields[i], bins=1000, density=True, histtype='step')
            ax_hist[i].set_xlabel(names[i])
            ax_hist[i].set_yscale('log')
            if save_pdfs:
                np.save(path + names[i] + '_' + name + '_ pdf.npy', pdf)
                np.save(path + names[i] + '_' + name + '__bins.npy', bins)
                
        fig_im.savefig(path + pl_name + '_2d', dpi=200)
        

        fig_hist.savefig(path +  pl_name + '_hist', dpi=200)
        

        
    else: 
        
        fig_im, ax_im  = pl.subplots(ncols=2, nrows=2) 
        fig_hist, ax_hist  = pl.subplots(ncols=2, nrows=2) 
        
        pl_name = 'all_obs_' + name
        
        pos = [(0, 0), (0, 1), (1, 0), (1, 1), ]
        
        for i in range(n_plots):
        
            j, k = pos[i] 
            ax_im[j, k].imshow(fields[i], 
                  cmap=get_cmap(cmaps[i]), 
                )
            ax_im[j, k].set_title(names[i])
            mappable = ax_im[j, k].get_images()[0]
            fig_im.colorbar(mappable, ax=ax_im[j, k])
            
            pdf, bins, _ = ax_hist[j, k].hist(fields[i].flatten(), bins=1000, density=True, histtype='step')
            ax_hist[j, k].set_xlabel(names[i])
            ax_hist[j, k].set_yscale('log')
            if save_pdfs:
                np.save(path + names[i] + '_' + name + '_pdf.npy', pdf)
                np.save(path + names[i] + '_' + name + '_bins.npy', bins)
                
        fig_im.savefig(path + pl_name + '_2d', dpi=200)
        

        fig_hist.savefig(path +  pl_name + '_hist', dpi=200)
        
    pl.close('all')
    return
    