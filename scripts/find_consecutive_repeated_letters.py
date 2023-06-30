
import pandas as pd
from Bio import SeqIO

def find_consecutive_repeated_letters(file_path):
    # Read the FASTA file and extract the sequence
    record =  SeqIO.read(file_path, 'fasta')
    organism = record.description.split('[')[1]
    geneid = record.description.split('[')[2]
    sequence = record.seq

    # Initialize variables
    repeats = []
    prev_char = ''
    start_index = -1
    curr_char = ''

    # Iterate over each character in the sequence
    for i, char in enumerate(sequence):
        # Check if the current character is the same as the previous character
        if char == prev_char:
            # If it's a repeated letter, update the start index and the current repeated letter
            if start_index == -1:
                start_index = i - 1
            curr_char = char
        else:
            # If the previous character was a repeated letter, store its information
            if start_index != -1:
                length = i - start_index
                repeat_info = {
                    'Letter': curr_char,
                    'Start': start_index + 1,  # Adjust start index by adding 1
                    'Length': length
                }
                repeats.append(repeat_info)
                start_index = -1

            curr_char = char

        prev_char = char

    # Check if the last character was a repeated letter
    if start_index != -1:
        length = len(sequence) - start_index
        repeat_info = {
            'Letter': curr_char,
            'Start': start_index + 1,  # Adjust start index by adding 1
            'Length': length
        }
        repeats.append(repeat_info)

    # Create a DataFrame from the repeats list
    repeats_df = pd.DataFrame(repeats)
    repeats_df["Accession"] = file_path.rsplit("/",1)[-1]
    repeats_df["Organism"] = organism[9:-2]
    repeats_df["Geneid"] = geneid[6:-1]

    return repeats_df
