#! /usr/bin/python3

import os
import re
import argparse

# arguments
parser = argparse.ArgumentParser(description="Extract repeat information from a FASTA gene sequence")
parser.add_argument("input_file", help="Input FASTA file")
parser.add_argument("output_file", help="Output file name for storing the repeat information")
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file

# regular expression pattern to extract the repeat sequence and unit information from <> and number directly after <>
pattern = r"<([^>]*)>(\d+)"

# basename of input fasta file to get gene name
input_basename = os.path.splitext(os.path.basename(input_file))[0]

# open the input FASTA file
with open(input_file, "r") as fasta_file:
    # Open the output file in write mode
    with open(output_file, "w") as tsv_file:
        # Write the header row
        tsv_file.write("Accession\tRepeat_Sequence\tRepeat_Unit\n")

        # Iterate over the lines in the file
        for line in fasta_file:
            # Check if the line starts with '>'
            if line.startswith("> #Info"):
                # Extract repeat and unit information using regex
                matches = re.findall(pattern, line)
                if matches:
                    for repeat, unit in matches:
                        tsv_file.write(f"{input_basename}\t{repeat}\t{unit}\n")
