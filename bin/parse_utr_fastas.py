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

# regular expression pattern to extract the repeat sequence and unit information
pattern = r"<([^>]*)>"

# basename of input fasta file to get gene name
input_basename = os.path.splitext(os.path.basename(input_file))[0]

# open the input FASTA file
