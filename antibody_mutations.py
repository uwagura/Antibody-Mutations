import h5py
import numpy as np
import os
import pandas as pd
import scipy as sp
import scipy.special
from zernike import *
import matplotlib.pyplot as plt
from helpers import *


# Create relevant dictionaries for mapping amino acid names to their other forms

aa_to_one_letter = {'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E',
                        'PHE': 'F', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
                        'LYS': 'K', 'LEU': 'L', 'MET': 'M', 'ASN': 'N',
                        'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', 'SER':'S',
                        'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'}

one_letter_to_aa = {'A': 'ALA', 'C': 'CYS',  'D': 'ASP',  'E': 'GLU',  'F': 'PHE',  'G': 'GLY',  'H': 'HIS',  'I': 'ILE',  'K': 'LYS',  'L': 'LEU',  'M': 'MET',  'N': 'ASN',  'P': 'PRO',  'Q': 'GLN',  'R': 'ARG',  'S': 'SER',  'T': 'THR',  'V': 'VAL',  'W': 'TRP',  'Y': 'TYR'}

aa_to_ind_size = {'CYS': 2, 'ILE': 8, 'GLN': 12, 'VAL': 6, 'LYS': 13,
       'PRO': 4, 'GLY': 0, 'THR': 5, 'PHE': 16, 'GLU': 14,
       'HIS': 15, 'MET': 11, 'ASP': 7, 'LEU': 9, 'ARG': 17,
       'TRP': 19, 'ALA': 1, 'ASN': 10, 'TYR': 18, 'SER': 3}

ind_to_aa_size = {0: 'GLY', 1: 'ALA', 2: 'CYS', 3: 'SER', 4: 'PRO',
       5: 'THR', 6: 'VAL', 7: 'ASP', 8: 'ILE', 9: 'LEU',
       10: 'ASN', 11: 'MET', 12: 'GLN', 13: 'LYS', 14: 'GLU',
       15: 'HIS', 16: 'PHE', 17: 'ARG', 18: 'TYR', 19: 'TRP'}

aa_to_ind_one_letter = {'ALA': 0, 'CYS': 1, 'ASP': 2, 'GLU': 3,
                        'PHE': 4, 'GLY': 5, 'HIS': 6, 'ILE': 7,
                        'LYS': 8, 'LEU': 9, 'MET': 10, 'ASN': 11,
                        'PRO': 12, 'GLN': 13, 'ARG': 14, 'SER':15,
                        'THR': 16, 'VAL': 17, 'TRP': 18, 'TYR': 19}

background_freqs = {'ALA': 7.4, 'CYS': 3.3, 'ASP': 5.9, 'GLU': 3.7,
                        'PHE': 4., 'GLY': 7.4, 'HIS': 2.9, 'ILE': 3.8,
                        'LYS': 7.2, 'LEU': 7.6, 'MET': 1.8, 'ASN': 4.4,
                        'PRO': 5., 'GLN': 5.8, 'ARG': 4.2, 'SER': 8.1,
                        'THR': 6.2, 'VAL': 6.8, 'TRP': 1.3, 'TYR': 3.3}

ind_to_aa_one_letter = {0: 'ALA', 1: 'CYS', 2: 'ASP', 3: 'GLU',
                        4: 'PHE', 5: 'GLY', 6: 'HIS', 7: 'ILE',
                        8: 'LYS', 9: 'LEU', 10: 'MET', 11: 'ASN',
                        12: 'PRO', 13: 'GLN', 14: 'ARG', 15: 'SER', 
                        16: 'THR', 17: 'VAL', 18: 'TRP', 19: 'TYR'}

aa_to_ind_hydro = {'ALA': 8, 'ARG': 15, 'ASN': 17, 'ASP': 14,
                   'CYS': 6, 'GLN': 13, 'GLU': 10, 'GLY': 11,
                   'HIS': 18, 'ILE': 1, 'LEU': 0, 'LYS': 16,
                   'MET': 5, 'PHE': 2, 'PRO': 19, 'SER': 12,
                   'THR': 9, 'TRP': 3, 'TYR': 7, 'VAL': 4}

ind_to_aa_hydro = {8: 'ALA', 15: 'ARG', 17: 'ASN', 14: 'ASP',
                   6: 'CYS', 13: 'GLN', 10: 'GLU', 11: 'GLY',
                   18: 'HIS', 1: 'ILE', 0: 'LEU', 16: 'LYS', 
                   5: 'MET', 2: 'PHE', 19: 'PRO', 12: 'SER',
                   9: 'THR', 3: 'TRP', 7: 'TYR', 4: 'VAL'}

# Create list of proteins of interest
control_proteins = ["1ad0", "1ad9", "1adq", "1aqk", "1bbj", "1bey", "1bvk", "1dee", "1dl7", "1dn0", "1dql", "1fvd", "1gaf", "1h0d", "1i9r", "1igm", "1iqd", "1jpt", "1jv5", "1kfa", "1l7i", "1mco", "1mim", "1nl0", "1rz7", "1t3f", "1u6a", "1uj3", "1vge", "1w72", "1wt5", "1za6", "2agj", "2aj3", "2b1h", "2cmr", "2d7t", "2eiz", "2fee", "2fjh", "2fl5", "2g75", "2h9g", "2j6e", "2jb5", "2qqk", "2qqn", "2qr0", "2qsc", "2r0k", "2r56", "2uzi", "2vxq", "2vxv", "2wuc", "2xa8", "2xra", "2xzc", "2yc", "2zkh", "3aaz", "3d85", "3dgg", "3dif", "3dvg", "3eo9", "3g04", "3g6a", "3giz", "3gjf", "3gkw", "3go1", "3h0t", "3h42", "3hc3", "3hc4", "3hi6", "3hmx", "3k2u", "3kdm", "3kr3", "3kym", "3l5y", "3ma9", "3mlr", "3mxw", "3n85", "3n9g", "3na9", "3ncj", "3nfs", "3nh7", "3oaz", "3p0y", "3pgf", "3qcu", "3qot", "3r1g", "3sdy", "3se9", "3sqo", "3t2n", "3tnm", "3tnn", "3u0t", "3u30", "3uji", "3ujj", "3uls", "3wd5", "4d9l", "4d9q", "4dag", "4dgy", "4dke", "4dkf", "4dtg", "4fqi", "4g3y", "4g5z", "4g6a", "4g6m", "4gsd", "4hcr", "4hfu", "4hfw", "4hg4", "4hie", "4hj0", "4hpy", "4hs6", "4hs8", "4i77", "4j6r", "4jam", "4jpi", "4jzn", "4ky1", "4lmq", "4lst", "4lsu"]

naive_proteins = [ "2XZA", "3EYQ", "3F12", "3QOS", "3QOT", "4JPI", "4JDV", "3EYQ", "3F12"]

# Save protein lists into hspherical_df5 file
proteins = h5py.File('proteins.hspherical_df5','w')
control = f.create_dataset("pdb_list_control", data = np.array(control_proteins))
naive = f.create_dataset("pdb_list_naive", data = np.array(naive_proteins))

print("created h5py file")

# Get the structural info for each protein, save it to a hspherical_df5 file
!python get_structural_info.py \
--hspherical_df5_out ../output/structure.hdf5 --pdb_list pdb_list_control \
--parallelism 20 --hspherical_df5_in  proteins.hdf5\
--pdb_dir ../output

# # Initialize hspherical_df5 file to hold neighborhood info
# spherical_coord = h5py.File("spherical_coordinates.hspherical_df5", 'w')
# pspherical_df_list_nbhoods = nbhoods.create_dataset("pdb_list_nbhoods")

# # Get relevant neighborhoods for each protein
# !python get_neighborhoods.py \
#     --hspherical_df5_out neighborhoods.hdf5 \
#     --protein_list pdb_list_nbhoods --parallelism 40 --hspherical_df5_in ../ouput/structure.hdf5 \
#     --num_nhs 10000 --r_max=10

# Initialize hspherical_df5 file to hold amino acid info
aa = h5py.File("aa_info.hdf5")
aa_set = aa.create_dataset("aa_list")

# Generate amino acids from proteins
!python get_amino_acids.py \
    --hspherical_df5_out aa_info.hdf5 \
    --protein_list aa_list --parallelism 40 --hspherical_df5_in spherical_coordinates.hdf5 --num_nhs 10000

# Get amino acid data, save as pandas dataframe
with h5py.File(f'results/alpha_protein_complete.hdf5','r') as f:
    val_aas = f['val_pdb_list'][:]

structural_dict = {x:[] for x in ['res_id','atom_names','elements','r','t','p','charges','SASAs','x','y','z']}
for aas in val_aas:
    if aas['res_id'][0] == b'':
        continue
    id = b''.join(aas['res_id'])
    #print(id)
    for i in range(30):    
        for info in aas.dtype.names:
            try:
                if aas[info] == b'':
                    continue
            except:
                a = 1
            #print(info)
            if info == 'res_id' or info == 'res_ids':
                continue
            if info == 'coords':
                structural_dict['r'].append(aas[info][i][0])
                structural_dict['t'].append(aas[info][i][1])
                structural_dict['p'].append(aas[info][i][2])
                structural_dict['x'].append(
                    aas[info][i][0]*np.sin(aas[info][i][1])*np.cos(aas[info][i][2])
                )
                structural_dict['y'].append(
                    aas[info][i][0]*np.sin(aas[info][i][1])*np.sin(aas[info][i][2])
                )
                structural_dict['z'].append(
                    aas[info][i][0]*np.cos(aas[info][i][1])
                )
            else:
                if info in ['atom_names','elements']:
                    structural_dict[info].append(aas[info][i].decode('utf-8'))
                else:
                    structural_dict[info].append(aas[info][i])
        structural_dict['res_id'].append(id)
        #print(structural_dict)
structural_spherical_df = pd.DataFrame(structural_dict)

# Convert amino acid data to holograms
holograms = h5py.File("holograms.hspherical_df5","w")
holo_set = holograms.create_dataset("zernike_list")
!python get_holograms_zach.py\
    --hspherical_df5_out holograms.hdf5 \
    --neighborhood_list zernike_list \
    --hspherical_df5_in holograms.hdf5\
    --Lmax 10 -k 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 \
    --r_max 10. \
    --num_nhs 10000

# TODO: Update this description
spherical_points = spherical_df[spherical_df['elements'] != ''][spherical_df['res_id'] == res1][spherical_df['elements'] == 'C'][['r','t','p']].to_numpy()
spherical_points[:,0] = spherical_points[:,0]/10.

# TODO: Update this description
n_points = len(spherical_points)
fig,axes = plt.subplots(int(n_points/2)+1,2,figsize=(10,7),dpi=100,)
max_val = 0.
# fig.set_layout('tight')
N = 50 # number of points in plot
for j,R in enumerate(spherical_points[:,0]):
    func = np.zeros(shape=(N))
    t = spherical_points[j,1]
    p = spherical_points[j,2]
#     print(t,p,R)
    for i,r in enumerate(np.linspace(0.,.9999,N)):

        total = 0
        for n in range(n_max):
            for l in range(l_max):
                for im,m in enumerate(range(-l,l+1)):
                    func[i] += np.conjugate(zernike_coeff_lm(r,t,p,n,1.,l,m)) * coeffs[l][n][im]
        #mesh[i,j] = total
    max_val = np.max((max_val,np.max(np.abs(func))))
    axes[j//2,j%2].plot(np.linspace(0,1.,50),np.abs(func))
    axes[j//2,j%2].axvline(x=R)
    axes[j//2,j%2].set_xlabel('r')
    axes[j//2,j%2].set_ylabel('|f|')
    axes[j//2,j%2].set_title(r'$\theta = {1:.3f}, \phi = {0:.3f}$'.format(p,t))
plt.tight_layout()
plt.show();



