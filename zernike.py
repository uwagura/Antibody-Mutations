#---------------------------------
# Functions for Zernike projection
#---------------------------------

import numpy as np
import scipy as sp
import scipy.special

# Inputs r,t,p in the shapes (ch X n) and give coefficients
# in output shape (ch)
def zernike_coeff_lm(r,t,p, n,r_max,l,m):
    # zernike coefficient is zero if n-l odd
    if (n-l) % 2 == 1:
        return 0.+0j

#     # check input dimensions of arrays
#     if (np.array(r).shape != np.array(t).shape or
#         np.array(t).shape != np.array(p).shape):
#         print('Error: input arrays do not have same shape')

    # dimension of the Zernike polynomial
    D = 3.
    # constituent terms in the polynomial
    A = np.power(-1,(n-l)/2.) 
    B = np.sqrt(2.*n + D)
    C = sp.special.binom(int((n+l+D)/2. - 1),
                         int((n-l)/2.))
    E = sp.special.hyp2f1(-(n-l)/2.,
                           (n+l+D)/2.,
                           l+D/2.,
                           np.array(r)/r_max*np.array(r)/r_max)
    F = np.power(np.array(r)/r_max,l)

    # spherical harmonic component
    y = np.conj(sp.special.sph_harm(m,l,p,t))
    
    # assemble coefficients
    coeffs = A * B * C * E * F * y 

    return np.sum(coeffs,axis=-1)
    
# Inputs r,t,p in the shapes (ch X n) and give coefficients
# in output shape (ch) 
def zernike_coeff_l(r,t,p,n,r_max,l):
    if (np.array(r).shape != np.array(t).shape or
        np.array(p).shape != np.array(t).shape):
        print('Error: input arrays do not have same shape')
        return None

    fourier_coeff_l = []
    for m in range(0,2*l+1):
        fourier_coeff_l.append(zernike_coeff_lm(r,t,p,n,r_max,l,m-l))
    return np.array(fourier_coeff_l)


def zernike_coeff_lm_new(r, t, p, n, r_max, l, m, weights):
    
#     # check input dimensions of arrays
#     if (np.array(r).shape != np.array(t).shape or
#         np.array(t).shape != np.array(p).shape):
#         print('Error: input arrays do not have same shape')

    # dimension of the Zernike polynomial
    D = 3.
    # constituent terms in the polynomial
    A = np.power(-1.0 + 0j, (n - l) / 2.)

    B = np.sqrt(2.*n + D)
    C = sp.special.binom((n+l+D) // 2 - 1,
                         (n-l) // 2)

    nl_unique_combs, nl_inv_map = np.unique(np.vstack([n, l]).T, axis=0,
                                            return_inverse=True)
    num_nl_combs = nl_unique_combs.shape[0]
    n_hyp2f1_tile = np.tile(nl_unique_combs[:, 0], (r.shape[1], 1)).T
    l_hyp2f1_tile = np.tile(nl_unique_combs[:, 1], (r.shape[1], 1)).T

    E_unique = sp.special.hyp2f1(-(n_hyp2f1_tile - l_hyp2f1_tile) / 2.,
                                 (n_hyp2f1_tile + l_hyp2f1_tile + D) /2.,
                                 l_hyp2f1_tile + D / 2.,
                                 r[:num_nl_combs, :]**2 / r_max**2)
    E = E_unique[nl_inv_map]
    
    l_unique, l_inv_map = np.unique(l, return_inverse=True)
    l_power_tile = np.tile(l_unique, (r.shape[1], 1)).T
    F_unique = np.power(r[:l_unique.shape[0]] / r_max, l_power_tile)
    F = F_unique[l_inv_map]

    # spherical harmonic component
    lm_unique_combs, lm_inv_map = np.unique(np.vstack([l, m]).T, axis=0,
                                            return_inverse=True)
    num_lm_combs = lm_unique_combs.shape[0]
    l_sph_harm_tile = np.tile(lm_unique_combs[:, 0], (p.shape[1], 1)).T
    m_sph_harm_tile = np.tile(lm_unique_combs[:, 1], (p.shape[1], 1)).T
    
    y_unique = np.conj(sp.special.sph_harm(m_sph_harm_tile, l_sph_harm_tile,
                                           p[:num_lm_combs], t[:num_lm_combs]))
    y = y_unique[lm_inv_map]
    
    if True in np.isinf(E):
        print('Error: E is inf')
        print('E',E)
        print('n',n,
              'l',l,
              'D',D,
              'r',np.array(r),
              'rmax',r_max)

    # assemble coefficients
    coeffs = A * B * C * np.einsum('N,nN,nN,nN->n', weights, E, F, y, optimize=True)

    return coeffs


