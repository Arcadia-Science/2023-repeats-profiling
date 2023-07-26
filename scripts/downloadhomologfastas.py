import pandas as pd

import os
import subprocess
import zipfile
import itertools
import shutil

import time
from tqdm import tqdm

## define a small function for iterating over batches
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

def downloadhomologfastas(BLAST_filepath,output_folder_path= "../results/hit_DNA_sequences",n_per_search=500, overwrite=False):

    """\
    This script takes a .csv file of protein BLAST results and downloads the corresponding nucleotide
    and protein fastas, putting them in a new folder (default = results/hit_DNA_sequences) with subfolders
    named for the gene that was BLASTed. To increase speed and reduce NCBI searches it searches in batches of
    n_per_search (default = 500).

    Usage: downloadhomologfastas.py BLAST_filepath output_folder_path n_per_search
    """
    #load Blast results
    results_df = pd.read_csv(BLAST_filepath)
    filtered_results = results_df[results_df["Accession"].str.startswith(('XP','NP'))] #only proteins with NCBI accessions (XP or NP) can be used

    #make folders of nucleotide sequences by queried gene
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
    for gene in filtered_results["gene"].unique():
        gene_folder = os.path.join(output_folder_path,gene)
        if not os.path.exists(gene_folder):
            os.mkdir(gene_folder)

    #pull down nucleotide and amino acid sequence for each protein hit

    for gene in filtered_results["gene"].unique():
        indv_gene = filtered_results[filtered_results["gene"] == gene]

        #get list of blast hits to download .fan files
        hits_to_find = list(map(''.join, indv_gene[["Accession"]].values.tolist()))

        fileidx = 0
        for these_accessions in tqdm(batched(hits_to_find, n_per_search)):
            accession_list = ' '.join(these_accessions)

            #make an iterator to append to batch file outputs
            fileidx += 1
            output_folder = os.path.join(output_folder_path,gene)


            #the downloaded results will be moved into the folder with an iterator appended
            new_gene_file = os.path.join(output_folder,'gene_list_batch'+ str(fileidx)+'.fna')
            new_protein_file = os.path.join(output_folder,'protein_list_batch'+ str(fileidx)+'.faa')

            if not overwrite:
                if os.path.exists(new_gene_file): continue

            #get nucleotide sequences
            search_query = "datasets download gene accession " + accession_list + " --include gene --include protein"
            subprocess.run(search_query, capture_output=True, shell=True, cwd=output_folder)

            #unzip results
            try:
                with zipfile.ZipFile(os.path.join(output_folder, 'ncbi_dataset.zip'), 'r') as zip_ref:
                    zip_ref.extractall(output_folder)
            except:
                continue

            ## move fastas and cleanup
            gene_file = f'{output_folder}/ncbi_dataset/data/gene.fna'
            os.rename(gene_file,new_gene_file)

            protein_file = f'{output_folder}/ncbi_dataset/data/protein.faa'
            os.rename(protein_file,new_protein_file)


            shutil.rmtree(f'{output_folder}/ncbi_dataset/')
            os.remove(f'{output_folder}/ncbi_dataset.zip')

            time.sleep(10) #try to avoid getting banned from making NCBI searches
