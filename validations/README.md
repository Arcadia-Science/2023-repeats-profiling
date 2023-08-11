# Validating Short-Read Generated Protein Hits with Corresponding Long-Read Assemblies

For some of the proteins we found hits to our disease-causing repeat expansion proteins, the gene/protein was generated from a short-read assembly. This could potentially have issues because short-read assemblers don't handle repeats very well and collapse them irreversibly. For hits that we found in short-read generated genes we wanted to confirm them in either related species or exact species with long-read assembly data available. From what we could find, this was available for 2 of our species in the hit list for 3 proteins (1 species has 2 hit proteins to confirm). These genome and gene accessions are listed in the `species_validation_list.csv` file.

Importantly, we couldn't find gene annotation information for these new assemblies, so we have to BLAST for candidate regions in these assemblies that could potentially be our gene of interest that we retrieved from the short-read assembly for this species hit.

## BLAST genes against the species genomes
For both species genomes, make nucleotide BLAST databases with:

```
makeblastdb -in $genomefasta -dbtype nucl
```

Then query the appropriate gene against the species database with:

```
blastn -query $genefasta -db $genomedb -outfmt 7 -out $genefasta-vs-$genomedb-results.tsv
```

For these genes we pulled down the whole scaffold that the gene was originally annotated from to have a better chance of BLASTing in the unannotated long-read genome. Where the results look like for example:
```
# BLASTN 2.14.0+
# Query: NW_011888994.1:3637973-3643487 Pteropus vampyrus isolate Shadow unplaced genomic scaffold, Pvam_2.0 Scaffold213, whole genome shotgun sequence
# Database: blast_dbs/GCA_902729225.1_Ma_sr-lr_union100_genomic.fna
# Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
# 1 hits found
NW_011888994.1:3637973-3643487	CACVBW010001364.1	99.583	5516	8	8	1	5515	369884	364383	0.0	10045
# BLAST processed 1 queries
```

For the other comparisons there are multiple hits, and we could filter by only selecting the top hit, but the other two queries only had about 7-8 total hits so we will go ahead and extract all those sequences from the full genome.

## Extracting the BLAST hit sequences from the genome FASTA file
The script `scripts/parse-blast-validations.py` takes in a BLAST TSV file from `outfmt 7` and the corresponding genome FASTA file that the BLAST result is from, and for every hit in the BLAST table extracts that range of sequence from the genome FASTA file into an individual FASTA file (most are 100-1000 bps, very small). The usage is `python3 scripts/parse-blast-validations.py <BLAST_TABLE> <GENOME_FASTA> <OUTDIR>` where for this since each BLAST table vs genome FASTA pair has to be processed separately, I've created separate subdirectory outputs for each gene query comparison.
