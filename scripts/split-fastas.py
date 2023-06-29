#! /usr/bin/python3

import os
import argparse
from Bio import SeqIO


def split_fasta(fasta_file, output_dir):
    with open(fasta_file, 'r') as original_fasta:
        records = SeqIO.parse(original_fasta, 'fasta')

        for record in records:
            # The description field contains the full FASTA header
            header = record.description
            filename = os.path.join(output_dir, header.split(':')[0] + '.fasta')

            # modify record header to container everything before : to simplify
            record.id = header.split(':')[0]
            record.description=''
            # Write each sequence to a new FASTA file
            with open(filename, 'w') as output_fasta:
                output_fasta.write(f">{record.id}\n{record.seq}\n")


def main():
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(description='Split a FASTA file into multiple files')
    parser.add_argument('input_file', help='The input FASTA file')
    parser.add_argument('output_dir', help='The output directory')

    # Parse the arguments
    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Call the function with the provided arguments
    split_fasta(args.input_file, args.output_dir)

if __name__ == "__main__":
    main()
