import numpy as np
import nifty8 as ift
from copy import copy


def analyze_step(rm, i, q, u, stat_dict=None, n_moments=4, do_pi=False):
    fields = [rm, i, q, u]
    do_field = [not f is None for f in fields]
    
    if do_field[2] + do_field[3] == 2: 
        if do_pi:
            fields = [rm, i, q, np.sqrt(q**2 + u**2)] 
    else:
        do_pi = False
        
    names = ['RM', 'I', 'Q', 'PI'] if do_pi else ['RM', 'I', 'Q', 'U']
    
    map(fields.__delitem__, sorted(do_field, reverse=True))
    map(names.__delitem__, sorted(do_field, reverse=True))
    
    
    if stat_dict is None: 
        m_dict = {n: {str(i): list() for i in range(3, n_moments + 1)} for n in names}
        stat_dict = {'PS_calc': {n: list() for n in names}, 
                     'PS_fit': {n: list() for n in names}, 
                     'PDF_calc': {n: list() for n in names}, 
                     'PDF_bin_center': {n: list() for n in names}, 
                     'Moments': m_dict, 
                    }

    class ps_fit: 
        def  __init__(self, ps_param) -> None:
            self.ps_pos = ps_param[0]
            self.ps_model = ps_param[1]
        def __call__(self):
            return self.ps_model(self.ps_pos).exp().val
        
    for name, f in zip(names, fields): 
        ps = calc_power_spectra(f)
        k = ps.domain[0].k_lengths
        ps_param = fit_power_spectra(ps.log().val,  k , ps.domain)
  
        psf = ps_fit(ps_param)()
        
        pdf, bins,= np.histogram(f.flatten(), bins=1000, density=True)
        
        d = np.diff(bins) 
        x = d/2 + bins[:-1]
        
        mean = np.vdot(d, x*pdf)
        var = np.vdot(d, (x - mean)**2*pdf)
        
        for i in range(3, n_moments + 1):
            m = np.vdot(d, (x - mean)**(i)*pdf)/var**(i/2)
            stat_dict['Moments'][name][str(i)].append(abs(m))
        # print(stat_dict['Moments'][name])
        stat_dict['PS_calc'][name].append(ps.val)
        stat_dict['PS_fit'][name].append(psf)
        stat_dict['PDF_calc'][name].append(pdf)
        stat_dict['PDF_bin_center'][name].append(x)
        # stat_dict['Moments'][name].append(mom)
        # print(stat_dict['Moments'][name])
    return stat_dict
        
            
            

def calc_power_spectra(f):
    rg = ift.RGSpace(f.shape)
    hd = rg.get_default_codomain()
    ht = ift.HarmonicTransformOperator(hd, rg)
    ff = ift.Field(ift.makeDomain(rg), np.copy(f))
    ps = ift.power_analyze(ht.adjoint(ff))
    return ps




def fit_power_spectra(ln_p, k, dom, ln_p_std=1.):
    if not isinstance(ln_p_std, np.ndarray):
        ln_p_std = np.full(ln_p.shape, ln_p_std)
    dom = ift.makeDomain(dom)
    expander = ift.VdotOperator(ift.full(dom, 1)).adjoint

    sc_dom = ift.DomainTuple.scalar_domain()
    xi_amp = ift.FieldAdapter(sc_dom, 'xi_amp')
    amp_norm = ift.makeOp(ift.Field.full(sc_dom, ln_p[0]))
    addamp = ift.Adder(ift.Field.full(sc_dom,  ln_p[0]))
    log_amp = (addamp@amp_norm@xi_amp)

    xi_slope = ift.FieldAdapter(ift.DomainTuple.scalar_domain(), 'xi_slope')
    mtwo = ift.Adder(ift.Field.full(sc_dom, 2))
    slope = mtwo(2*xi_slope)

    xi_k0 = ift.FieldAdapter(ift.DomainTuple.scalar_domain(), 'xi_k0')
    log_k0 = xi_k0
    k0 = log_k0.exp()
    #k[0] = 1
    k = ift.Field(dom, k)
    k = ift.Adder(k)
    k_sum = k@expander@k0
    model = expander@log_amp - k_sum.log()*(expander@slope)

    ln_p = ift.Field(dom, ln_p)
    ln_p_std = ift.Field(dom, ln_p_std)
    ivcov = ift.makeOp(ln_p_std**(-2), dom)

    likelihood = ift.GaussianEnergy(data=ln_p, inverse_covariance=ivcov) @ model

    # Settings for minimization
    ic_newton = ift.DeltaEnergyController(
        name=None, iteration_limit=100, tol_rel_deltaE=1e-8)
    minimizer = ift.NewtonCG(ic_newton)

    # Compute MAP solution by minimizing the information Hamiltonian
    H = ift.StandardHamiltonian(likelihood)
    initial_position = ift.full(model.domain, 0.)
    H = ift.EnergyAdapter(initial_position, H, want_metric=True)
    H, convergence = minimizer(H)

    return H.position, model

def fit_histogram():
    return
    