# Antibody Mutations

This repo contains my initial work generating predictions on how antibodies will mutate using a [rotationally-equivariant Convulutional Neural Network](https://www.biorxiv.org/content/10.1101/2022.10.31.514614v1). The main script of interest in this repo is prot_processing.ipynb - this is where I made predictions
across all sites on the antibodies of interest. There are two other Jupyter notebooks in this repo. toy_aminoacid_tutorial.ipynb is a tutorial on how to use the CNN (Note: this notebook was written by Mike Pun at the University of Washington), while 
antibody_esm.ipynb is an unfinished script I wrote to make predictions on the antibodies using the [Facebook ESM protein langauge model]( https://github.com/facebookresearch/esm).  

All the other files are either helper scripts that I modified to run with prot_processing.ipynb, or files containing data that was produced while running the notebook. These scripts, like much of this repo, are heavily based on earlier work done by Mike Pun. The 
purpose of each file should be clear by going through the prot_processing notebook. 

If you run the prot_processing.ipynb, you should note that there is a step where a large dataframe containing data from all neighborhoods across all amino acids is saved. This 
data frame is a bit large ( ~ .5 GB), so I have omitted it from the repo. If you wish to avoid saving this data frame, simply comment out or skip the line in the notebook
that saves spherical_structure_df to a csv named either "ssdf.csv" or "ssdf_naive.csv". 

-Utheri Wagura ( Summer 2022 University of Washington REU student)
