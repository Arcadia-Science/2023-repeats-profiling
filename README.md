# Profiling Repeat Expansions across the Tree of Life

This repository contains code, workflows, results, and metadata files for exploring genes, proteins, and genomes with repeat expansions (REs), with a specific focus on finding REs in homologs of human proteins that have disease-causing REs (dREs).

## Analysis steps
Unless otherwise noted the [profilerepeats notebook](notebooks/profilerepeats.ipynb) is used as the main workflow and scripts are called through this notebook.

Large files that could not be hosted on Github can be downloaded from Zenodo DOI: [10.5281/zenodo.8180704](10.5281/zenodo.8180704)

# 1. Finding homologs and structurally similar proteins
To find homologs using protein BLAST run the [BLASTdREgenes notebook](notebooks/BLASTdREgenes.ipynb).ipynb notebook in Google Colab, saving the results in google drive before manually downloading it. Afterwards run the [countdREseqhomology notebook](notebooks/countdREseqhomology.ipynb)"to filter and count homologs of the BLAST results, which puts the results in the homology folder with the name dREhomologs_"date".csv . To find structurally similar proteins use FoldSeek and aggregate the results into a single file with the name dREstruct_similarity_"date".tsv placed in the homology folder.

# 2. Fasta downloading
To pull refseq fastas from our BLAST results, after downloading the[ NCBI's command line tools](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/) run the[ downlowdhomologfastas script](scripts/downloadhomologfastas.py).To get all accesions you must run the "Pulling" notebooks for homolog acccessions which can not be pulled down using the NCBI's command line tools. These include foldseek [amino acid](notebooks/Pulling_amino_acid_fasta_for_foldseek_results.ipynb) and [nucleotide](notebooks/Pulling_gene_sequences_from_foldseek_results.ipynb) sequences, as well as [genbank](notebooks/Pulling_amino_acid_fasta_from_genbank_for_foldseek_results.ipynb) BLAST accessions

# 3. Amino acid counting
To count amino acid repeats use the [fcrl script](scripts/fcrl.py) to count repeated amino acids for each set of fastas. Next to analyze the fasta use the [analyzecountedAAs script](scripts/analyzecountedAAs.py) script to
combine the fastas into a single folder, analyze them for repeats, and combine the analyzed repeats with homology metadata using the [analyzecountedAAs script](scripts/analyzecountedAAs.py).

# 4. Plotting
For plotting, use the [plotrepeats script](scripts/plotrepeats.py) to plot analyzed repeat counts for each set of dRE genes individually, and to violinplot repeats relative to repeat lengths in humans. To map onto taxonomic trees, first obtain counts for repeats exceeding the healthy human limits using the final cells in the [profilerepeats notebook](notebooks/profilerepeats.ipynb).  Counts relative to species taxid can then be plotted using the[tree plotting notebook](notebooks/NCBI_taxid_to_lineage_and_barchart_tree_plotting.ipynb).


## Nucleotide Counting Workflow
This repository includes a Nexflow workflow to process and summarize tandem repeats in input nucleotide FASTA files. To use the workflow, navigate to the `repeat_profiler_workflow` subdirectory and follow the installation and setup instructions there.
