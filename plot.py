import os
import matplotlib.pyplot as pl
from matplotlib import cm, colors
import numpy as np
from analysis import calc_power_spectra

def get_cmap(cm_string):
    if cm_string == '':
        return None
    cmap = getattr(cm, cm_string)
    return cmap

    
    
def gen_axis(n_plots, names, n_figs):
    figs = []
    axs = []
    if n_plots == 1:    
        for _ in range(n_figs):
            fig, ax  = pl.subplots(ncols=1, nrows=1)
            ax = np.asarray([ax,]).reshape((1, 1))
            figs.append(fig)
            axs.append(ax)
        coordinates = [(0 , 0), ]
        pl_name = names[0] + '_'
    elif n_plots == 2:
        for _ in range(n_figs):
            fig, ax  = pl.subplots(ncols=2, nrows=1)
            ax = np.asarray([ax,])
            figs.append(fig)
            axs.append(ax)
        coordinates = [(0 , 0), (0, 1)]
        pl_name = names[0] + names[1] + '_'
    else:
        for _ in range(n_figs):
            fig, ax  = pl.subplots(ncols=2, nrows=2)
            figs.append(fig)
            axs.append(ax)
        coordinates = [(0, 0), (0, 1), (1, 0), (1, 1), ]
        pl_name = ''
    return figs, axs, coordinates, pl_name
    

def save_obs(rm, i, q, u, path='./Results/', name='', do_pi=True):
    if len(name) > 0: 
        path  = path + name + '/'
        if not os.path.exists(path):
            os.makedirs(path)
    
    
    fields = [rm, i, q, u] 
    do_field = [not f is None for f in fields]
    names = ['RM', 'I', 'Q', 'PI'] if do_pi else ['RM', 'I', 'Q', 'U']

    n_plots = sum(do_field)
    
    map(fields.__delitem__, sorted(do_field, reverse=True))
    map(names.__delitem__, sorted(do_field, reverse=True))
    
    for i in range(n_plots):
        np.save(path + names[i], fields[i])


def plot_obs(rm, i, q, u, stat_dict, n_boxes, path='./Plot/', name='', save_pdfs=True, do_pi=True):
    
    pl.rcParams["axes.prop_cycle"] = pl.cycler("color", pl.cm.plasma(np.linspace(0, 1, n_boxes)))
    
    if len(name) > 0: 
        path  = path + name + '/'
        if not os.path.exists(path):
            os.makedirs(path)
    
    fields = [rm, i, q, u] 
    do_field = [not f is None for f in fields]
    
    if do_field[2] + do_field[3] == 1:
        raise ValueError('Thats odd, either both q and u should be given or None of them')
    
    if do_field[2] + do_field[3] == 2: 
        if do_pi:
            fields = [rm, i, q, np.sqrt(q**2 + u**2)] 
    else:
        do_pi = False
    
    cmaps = ['RdBu_r', 'viridis', 'magma', 'viridis'] if do_pi else ['RdBu_r', 'viridis', 'magma', 'magma']
    names = ['RM', 'I', 'Q', 'PI'] if do_pi else ['RM', 'I', 'Q', 'U']

    n_plots = sum(do_field)
    
    map(fields.__delitem__, sorted(do_field, reverse=True))
    map(names.__delitem__, sorted(do_field, reverse=True))
    map(cmaps.__delitem__, sorted(do_field, reverse=True))
    
    
        
    figs, axs, pos, pl_name = gen_axis(n_plots, names, 6)
    
    fig_im, fig_hist, fig_mom, fig_pdf, fig_ps, fig_ps_fit = figs
    ax_im , ax_hist, ax_mom, ax_pdf, ax_ps, ax_ps_fit  = axs
    
    pl_name +=  name
    
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
            
        moments = stat_dict['Moments'][names[i]]
        moments_colors = ['blue', 'red', 'green']
        moment_names = {"3": "skewness", "4": "kurtosis"}
        for jj, (n_mom, mom_arr) in enumerate(moments.items()):
            ax_mom[j, k].plot(mom_arr, label=moment_names[n_mom], c=moments_colors[jj])
        ax_mom[j, k].set_xlabel(names[i])  
        ax_mom[j, k].set_yscale('log')
        ax_mom[j, k].legend()  
        
        pdfs = stat_dict['PDF_calc'][names[i]]
        x = stat_dict['PDF_bin_center'][names[i]]
        for z, _pdf in enumerate(pdfs):
            ax_pdf[j, k].plot(x[z], _pdf, label=str(z))
        #ax_pdf[j, k].set_xlabel(names[i])  
        ax_pdf[j, k].set_yscale('log')
        #ax_pdf[j, k].legend()  

        pss = stat_dict['PS_calc'][names[i]]
        for z, _ps in enumerate(pss):
            ax_ps[j, k].plot(_ps/(z + 1), label=str(z))
        #ax_ps[j, k].set_xlabel(names[i])  
        ax_ps[j, k].set_yscale('log')
        ax_ps[j, k].set_xscale('log')
        #ax_ps[j, k].legend()  
        
        psf = stat_dict['PS_fit'][names[i]]
        for z, _psf in enumerate(psf):
            ax_ps_fit[j, k].plot(_psf/(z + 1), label=str(z + 1))
        # ax_ps_fit[j, k].set_xlabel(names[i])  
        ax_ps_fit[j, k].set_yscale('log')
        ax_ps_fit[j, k].set_xscale('log')
        # ax_ps_fit[j, k].legend()  
        
    pl.tight_layout()
    
    fig_pdf.suptitle("PDFs", fontsize=12)
    norm = colors.Normalize(vmin=0, vmax=n_boxes)
    fig_pdf.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.plasma), ax=ax_pdf, shrink=1.)

    
    fig_ps.suptitle("PS/n_boxes", fontsize=12)
    norm = colors.Normalize(vmin=0, vmax=n_boxes)
    fig_ps.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.plasma), ax=ax_ps, shrink=1.)

    
    fig_ps_fit.suptitle("Fitted PS/n_boxes", fontsize=12)
    norm = colors.Normalize(vmin=0, vmax=n_boxes)
    fig_ps_fit.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.plasma), ax=ax_ps_fit, shrink=1.)
            
    fig_im.savefig(path + pl_name + '_2d', dpi=200)
    fig_mom.savefig(path +  pl_name + '_moments', dpi=200)  
    fig_hist.savefig(path +  pl_name + '_hist', dpi=200)
    fig_pdf.savefig(path +  pl_name + '_pdfs', dpi=200)
    fig_ps.savefig(path +  pl_name + '_power_spectra', dpi=200)
    fig_ps_fit.savefig(path +  pl_name + '_power_spectra_fitted', dpi=200)
        
    pl.close('all')
    return
    