import os
from FaSplitter import FaSplitter

def arrangeouputfastas(fastas_directory="results/hit_DNA_sequences/"):
    """\
    This script takes a user-defined path to a tree structure with many
    combined nucleotide and protein fastas, and splits the combined fastas into seperate .fa files,
    and puts those files into a subdirectory with the name split_gene_fastas or split_protein_fastas

    Usage: ArrangeOuputFastas.py fastas_directory
    """

    for folder in os.scandir(fastas_directory):
        split_genes_folder = os.path.join(folder,'split_gene_fastas')
        split_proteins_folder = os.path.join(folder,'split_protein_fastas')
        folder_str = folder.path

        if "." in folder_str:
                        continue
        if not os.path.exists(split_genes_folder):
                os.mkdir(split_genes_folder)
        if not os.path.exists(split_proteins_folder):
                os.mkdir(split_proteins_folder)

        for file in os.scandir(folder):
                file_str = file.path
                if file_str.endswith(".fna"):
                        FaSplitter(file_str,split_genes_folder+"/")
                elif file_str.endswith(".faa"):
                        FaSplitter(file_str,split_proteins_folder+"/")
