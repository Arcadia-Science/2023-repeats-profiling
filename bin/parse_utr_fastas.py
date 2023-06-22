#! /usr/bin/python3

import os
import re
import argparse

# arguments
parser = argparse.ArgumentParser(description="Extract repeat information from a FASTA gene sequence")
parser.add_argument("input_files", nargs="+", help="Input directory of FASTA files containing repeat information")
parser.add_argument("output_file", help="Output file name for storing the repeat information")
args = parser.parse_args()

input_files = args.input_files
output_file = args.output_file

# regular expression pattern to extract the repeat sequence and unit information from <> and number directly after <>
pattern = r"<([^>]*)>(\d+)"

# open output summary TSV file
with open(output_file, "a") as tsv_summary:
    tsv_summary.write("Accession\tRepeat_Sequence\tRepeat_Unit\n")

    # iterate over input fastas in input directory
    for input_file in input_files:
        if input_file.endswith(".fasta"):
            input_basename = os.path.splitext(os.path.basename(input_file))[0]
            input_basename = input_basename.replace(".utr", "")

            # open input FASTA file
            with open(input_file, "r") as fasta_file:
                for line in fasta_file:
                    if line.startswith("> #Info"):
                        matches = re.findall(pattern, line)
                        if matches:
                            for repeat, unit in matches:
                                tsv_summary.write(f"{input_basename}\t{repeat}\t{unit}\n")
