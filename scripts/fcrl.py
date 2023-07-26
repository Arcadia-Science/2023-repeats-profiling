import os
import pandas as pd
from Bio import SeqIO

def fcrlwrapper(input_dir, output_folder, MRget=False, overwrite=False):

    for gene_folder in os.scandir(input_dir):

        if not gene_folder.is_dir(): continue

        if MRget: #How I arranged my data from NCBIget is unique
            directory = os.path.join(gene_folder,"split_protein_fastas")
            this_gene = gene_folder.path.rsplit('/')[-1]
        else:
            directory = gene_folder
            this_gene = gene_folder.path.rsplit('/')[-1].split('_')[0]

        save_name = os.path.join(output_folder, this_gene + ".csv")
        if not overwrite:
            if os.path.isfile(save_name): continue

        try:
            del all_rpt_cnts
        except:
            None

        for files in os.listdir(directory):
            if ".DS_Store" in files: continue
            file_path = os.path.join(directory, files)

            this_rpt_cnt = fcrl(file_path)

            try:
                all_rpt_cnts = pd.concat([all_rpt_cnts,this_rpt_cnt])
            except:
                all_rpt_cnts = this_rpt_cnt


        all_rpt_cnts.to_csv(save_name)

def fcrl(file_path):
    # Read the FASTA file and extract the sequence
    try:
        record =  SeqIO.read(file_path, 'fasta') #Genbank files can have record not found errors
    except:
        return

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

    return repeats_df


def combinecounts(input_folder1,input_folder2,output_folder,databases):
#combine two folder of counts (e.g folders with Refseq and Genbank counts)

    for files in os.listdir(input_folder1):
        if ".DS_Store" in files: continue
        file_path = os.path.join(input_folder1, files)
        this_gene = file_path.split('/')[-1]

        first_counts_set = pd.read_csv(file_path)
        if not "database" in first_counts_set:
            first_counts_set["database"] = databases[0]

        try:
            second_counts_set = pd.read_csv(os.path.join(input_folder2,this_gene))
        except: continue

        if not "database" in second_counts_set:
            second_counts_set["database"] = databases[1]

        combined_counts= pd.concat([first_counts_set,second_counts_set], ignore_index=True,verify_integrity=True)
        combined_counts.reset_index(drop=True, inplace=True)
        combined_counts.to_csv(os.path.join(output_folder,this_gene))
