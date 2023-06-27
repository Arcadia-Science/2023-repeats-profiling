#! /usr/bin/python3

import argparse
import os


def remove_N(input_file, output_extension):
    # Get output filename
    output_basename = os.path.splitext(input_file)[0]
    output_file = output_basename + output_extension

    with open(input_file, "r") as in_fasta, open(output_file, "w") as out_fasta:
        header = ""
        sequence = ""
        for line in in_fasta:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    # Write the previous record header and go to the sequence
                    cleaned_sequence = sequence.replace('N', '')  # Remove 'N' characters
                    if cleaned_sequence:
                        out_fasta.write(f"{header}\n{cleaned_sequence}\n")
                # Start of a new record
                header = line
                sequence = ""
            else:
                sequence += line

        # Write the last record
        cleaned_sequence = sequence.replace('N', '')  # Remove 'N' characters
        if cleaned_sequence:
            out_fasta.write(f"{header}\n{cleaned_sequence}\n")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="FASTA screening script")
    parser.add_argument("input_file", help="Input FASTA file")
    parser.add_argument("-e", "--extension", help="Output file extension", default=".screened.fasta")
    args = parser.parse_args()

    remove_N(args.input_file, args.extension)
