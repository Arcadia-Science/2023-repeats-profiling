import os
from Bio import SeqIO

def FaSplitter(path_to_fasta,output_folder):
    """\
    This script takes a user-defined path to a combined fasta file,
    splits the combined fasta into seperate .fa files,
    and puts those files into a user-defined directory

    Usage: FaSplitter.py path_to_fasta output_folder name
    """
    # Open the input FASTA file
    with open(path_to_fasta, "r") as handle:
        # Parse the FASTA file using SeqIO
        records = SeqIO.parse(handle, "fasta")

        # Iterate over each record
        for record in records:
            # Create a new filename based on the record ID
            output_file = f"{record.id}.fa"
            output_file = os.path.join(output_folder,output_file)

            # Save the record as a new FASTA file
            with open(output_file, "w") as output_handle:
                SeqIO.write(record, output_handle, "fasta")
