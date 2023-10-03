# antibody_mutations

Initial work generating predictions with Mike's model on antibodies. The main script of interest in this repo is prot_processing.ipynb - this is where I made predictions
across all sites on the antibodies of interest. There are two other Jupyter notebooks in this repo. toy_aminoacid_tutorial.ipynb is simply a copy of Mike's tutorial, while 
antibody_esm.ipynb is an unfinished script I wrote to make predictions on the antibodies using the ESM model. Mike's tutorial may be a useful reference for why things were 
done a certain way, but the esm script may not be super useful given how little of it is actually complete. 

All the other files are either helper scripts that I modified to run with prot_processing.ipynb, or files containing data that was produced while running the notebook. The 
purpose of the file should be clear by going through the prot_processing notebook, but if something is confusing, don't hesitate to reach out to me at utheriwagura@gmail.com.

Two last notes: there is a step in prot_processing.ipynb where a large dataframe containing info from all neighborhoods across all amino acids is saved. Turns out that this 
data frame is absurdly large ( ~ .5 GB), so I have omitted it from the repo. If you wish to avoid saving this data frame, simply comment out or skip the line in the notebook
that saves the spherical_structure_df to a csv named either "ssdf.csv" or "ssdf_naive.csv". 

The other note is that this repo was once part of a copy of Mike's much larger protein_holography directory. I think this repo contains all the necesary files to run 
prot_processing, but if something fails it may be because it depended on some file that was in Mike's directory. This should be fixable by simply copying over Mike's 
protein_holography directory, but if this still leads to weird dependency issues just reach out to me and I would be glad to help sort it out. 

-Utheri Wagura ( Summer 2022 REU student)


