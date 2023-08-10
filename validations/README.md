# Validating Short-Read Generated Protein Hits with Corresponding Long-Read Assemblies

For some of the proteins we found hits to our disease-causing repeat expansion proteins, the gene/protein was generated from a short-read assembly. This could potentially have issues because short-read assemblers don't handle repeats very well and collapse them irreversibly. For hits that we found in short-read generated genes we wanted to confirm them in either related species or exact species with long-read assembly data available. From what we could find, this was available for 2 of our species in the hit list for 3 proteins (1 species has 2 hit proteins to confirm). These genome and gene accessions are listed in the `species_validation_list.csv` file.

Importantly, we couldn't find gene annotation information for these new assemblies, so we have to BLAST for candidate regions in these assemblies that could potentially be our gene of interest that we retrieved from the short-read assembly for this species hit. After obtaining the BLAST hits we will run the short-read generated gene and long-read generated candidates through the repeat profiler workflow to see if we find regions with the same or similar repeat profiles as the original hit gene had.

## BLAST genes against the species genomes
For both species genomes, make nucleotide BLAST databases with:

```
makeblastdb -in $genomefasta -dbtype nucl
```

Then query the appropriate gene against the species database with:

```
blastn -query $genefasta -db $genomedb -outfmt 7 -out $genefasta-vs-$genomedb-results.tsv
```

Where the results look like:
```
# BLASTN 2.14.0+
# Query: lcl|NW_011888994.1_cds_XP_011371116.1_1 [gene=PABPN1] [db_xref=GeneID:105300542] [protein=polyadenylate-binding protein 2] [protein_id=XP_011371116.1] [location=join(3638824..3639177,3639538..3639652,3640348..3640415,3640730..3640836,3641313..3641400,3641489..3641640,3642575..3642614)] [gbkey=CDS]
# Database: blast_dbs/GCA_902729225.1_Ma_sr-lr_union100_genomic.fna
# Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
# 7 hits found
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	99.164	359	3	0	6	364	369031	368673	0.0	647
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	100.000	155	0	0	731	885	366373	366219	5.59e-75	287
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	99.160	119	1	0	354	472	368323	368205	2.68e-53	215
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	100.000	109	0	0	538	646	367130	367022	2.08e-49	202
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	98.969	97	1	0	644	740	366548	366452	4.54e-41	174
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	100.000	71	0	0	469	539	367513	367443	2.77e-28	132
lcl|NW_011888994.1_cds_XP_011371116.1_1	CACVBW010001364.1	100.000	43	0	0	882	924	365288	365246	1.02e-12	80.5
# BLAST processed 1 queries
```

For this comparison there are 7 hits, for the other two there are similar numbers of hits, so not a lot to work with. For this one the hits have high sequence identity, for the other two there are only one or two hits with this high of sequence identity to the query. For the example above, the first hit has the best sequence identity and longest alignment length, where the rest the alignment length falls off quite a bit. We could in theory take the top hit in terms of sequence identity/alignment length/e-value/bitscore - but it's not super resource intensive to grab all these sequences into mini-fastas and process through the repeat-profiling workflow.

## Extracting the BLAST hit sequences from the genome FASTA file
The script `scripts/parse-blast-results.py` takes in a BLAST TSV file from `outfmt 7` and the corresponding genome FASTA file that the BLAST result is from, and for every hit in the BLAST table extracts that range of sequence from the genome FASTA file into an individual FASTA file (most are 100-1000 bps, very small). The usage is `python3 scripts/parse-blast-results.py <BLAST_TABLE> <GENOME_FASTA> <OUTDIR>` where for this since each BLAST table vs genome FASTA pair has to be processed separately, I've created separate subdirectory outputs for each gene query comparison. Within each subdirectory I've copied the original gene the repeat was identified in (from a short-read assembly) to directly compare the repeat profiles with.

Then run the repeat profiler workflow with:
```
nextflow run main.nf --input <QUERY_DIRECTORY> --outdir <QUERY_RESULTS>
```
