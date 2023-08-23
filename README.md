# Profiling Repeat Expansions across the Tree of Life

This repository contains code, workflows, results, and metadata files for exploring genes, proteins, and genomes with repeat expansions (REs), with a specific focus on finding REs in homologs of human proteins that have disease-causing REs (dREs).

## Analysis steps
Unless otherwise noted the [profilerepeats notebook](notebooks/profilerepeats.ipynb) is used as the main workflow and scripts are called through this notebook.

Large files that could not be hosted on Github can be downloaded from Zenodo DOI: [10.5281/zenodo.8180704](10.5281/zenodo.8180704)

# 1. Finding homologs and structurally similar proteins
To find homologs using protein BLAST run the [BLASTdREgenes notebook](notebooks/BLASTdREgenes.ipynb).ipynb notebook in Google Colab, saving the results in google drive before manually downloading it. Afterwards run the [countdREseqhomology notebook](notebooks/countdREseqhomology.ipynb)"to filter and count homologs of the BLAST results, which puts the results in the homology folder with the name dREhomologs_"date".csv . To find structurally similar proteins start by pulling human disease-related expansion protein Alphafold strucures, if they in the protein databank. For proteins without an Alphafold structure, if they are less than 400 amino acids fold them using an ESMfold API query. If they are larger than 400 amino acids obtain a structure from UniProt. Once PDB files are pulled down, use query query the Foldseek web API using the AlphaFold/Uniprot50 v4, AlphaFold/Swiss-Prot v4, and AlphaFold/Proteome v4 databases with a maximum of 1000 hits returned per database.

# 2. Fasta downloading
To pull refseq fastas from our BLAST results, after downloading the[ NCBI's command line tools](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/) run the[ downlowdhomologfastas script](scripts/downloadhomologfastas.py).To get all accesions you must run the "Pulling" notebooks for homolog acccessions which can not be pulled down using the NCBI's command line tools. These include foldseek [amino acid](notebooks/Pulling_amino_acid_fasta_for_foldseek_results.ipynb) and [nucleotide](notebooks/Pulling_gene_sequences_from_foldseek_results.ipynb) sequences, as well as [genbank](notebooks/Pulling_amino_acid_fasta_from_genbank_for_foldseek_results.ipynb) BLAST accessions

# 3. Amino acid counting
To count amino acid repeats use the [fcrl script](scripts/fcrl.py) to count repeated amino acids for each set of fastas. Next to analyze the fasta use the [analyzecountedAAs script](scripts/analyzecountedAAs.py) script to
combine the fastas into a single folder, analyze them for repeats, and combine the analyzed repeats with homology metadata using the [analyzecountedAAs script](scripts/analyzecountedAAs.py).

# 4. Plotting
For plotting, use the [plotrepeats script](scripts/plotrepeats.py) to plot analyzed repeat counts for each set of dRE genes individually, and to violinplot repeats relative to repeat lengths in humans. To map onto taxonomic trees, first obtain counts for repeats exceeding the healthy human limits using the final cells in the [profilerepeats notebook](notebooks/profilerepeats.ipynb).  Counts relative to species taxid can then be plotted using the[tree plotting notebook](notebooks/NCBI_taxid_to_lineage_and_barchart_tree_plotting.ipynb).


## Nucleotide Counting Workflow
This repository includes a Nexflow workflow to process and summarize repeats in input nucleotide FASTA files. To use the workflow, you will need to have Docker and Nextflow installed:
1. Install Docker [according to these instructions for your operating system](https://docs.docker.com/engine/install/).
2. The easiest way to install Nextflow without worrying about dependency issues on your machine is through a conda environment, and can [install according to the instructions for your operation system](https://docs.conda.io/en/latest/miniconda.html).

Once you have these installed, you can set up the workflow with:

```
git clone https://github.com/Arcadia-Science/REprofile.git
cd REprofile #move into repository folder
```

```
conda env create -n nextflow -f envs/nextflow_environment.yml
conda activate nextflow
```

To run the workflow, you need to provide an input directory of nucleotide FASTA files where each FASTA file is a single record or gene. Input file names should end in '.fasta'. If you have a multi-FASTA file containing several genes where the header is the name of the gene, you can use the script `python3 scripts/split-fastas.py multifasta.fasta fasta_directory/` which will produce individual FASTA files per record in the output directory. Use this directory as your input directory for the workflow:

```
nextflow run main.nf --input fasta_directory --outdir repeat_results
```

- The workflow first screens each input FASTA file for "N" characters and removes these, as the repeat profiling tool will error out if there are anything but expected nucleotide characters in the file.
- Then repeats are profiled with the [uTR](https://github.com/morisUtokyo/uTR) tool. Importantly, a fork of this tool was created to modify the `MAX_READS_LENGTH` parameter to `1000000` from the default `20000` since most the input genes we were working with were above this length. This fork is available [here](https://github.com/elizabethmcd/uTR) and is what the Docker image is built off of.
- Repeats are summarized into a single TSV file. Intermediate files and results are found in subdirectories of the output results directory in `screened` for the screened FASTAs, `utr` for the raw uTR result files, and `summary` with the final summary TSV file.


Repeats are summarized into a single TSV file that looks like:
```
Accession	Repeat_Sequence	Repeat_Unit	Repeat_Extension	Total_Repeat_Length
NW_020955290.1	AC	2	20	40
NW_020955290.1	AG	2	20	40
NW_020955290.1	AC	2	25	50
NW_020955290.1	AG	2	17	34
NW_020955290.1	CT	2	20	40
NW_020955290.1	AG	2	20	40
NW_020955290.1	CT	2	18	36
NW_020955290.1	AC	2	24	48
NW_020955290.1	CT	2	38	76
```

Where the `accession` is the name of the gene grabbed from the filename, the `repeat_sequence` is the actual sequence of the repeat-mer, the `repeat_unit` is the units of the actual repeat-mer, so 2 = repeat made up of 2 nucleotides, the `repeat_extension` is how many times the repeat is extended, and `total_repeat_length` is the `repeat_unit` multiplied by the `repeat_extension`.

## FAQs and Potential Errors
A successful start-up of the workflow should look like:
```
nextflow run main.nf --input fastas/2023-06-27-modified-fastas --outdir full_test

N E X T F L O W  ~  version 22.10.6
Launching `main.nf` [boring_venter] DSL2 - revision: 075466ffc3
PROFILE REPEAT EXPANSIONS IN GENE SEQUENCES
===========================================
input               : fastas/2023-06-27-modified-fastas
outdir              : full_test

executor >  local (330)
[d2/8f0cf0] process > screen_fastas (NW_022134904.1_screen) [100%] 263 of 263 ✔
[f6/fc726d] process > run_utr (NW_017731685.1_utr)          [ 24%] 64 of 263, failed: 1
```

And successful completion of the workflow looks like:
```
Completed at: 27-Jun-2023 16:09:11
Duration    : 21m 6s
Succeeded   : 189
Cached      : 326
Ignored     : 12
Failed      : 12
```
If you do not see the output summary shown above, but all steps have completed successfully and received checkmarks, everything should be good to go.
You will notice that some jobs fail at the `run_utr` process. This could be due to an input sequence being longer than the default of 1000000 bps, which has to be hardcoded into the original software, and any updates require the software to be recompiled and the Docker image rebuilt. If we find that many files are passing this threshold, we can update as needed.

To debug or look at the logs for which files fail certain steps, you can investigate in the `work/` directory or the most recent `.nextflow.log` file. A future improvement will be better tracking of which files don't pass the repeat profiling and making a list of those to investigate specifically why the failed. For now, the workflow is designed to keep going even if some files fail that step.
