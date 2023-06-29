import os
import pandas as pd
import argparse
import re

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process TSV files and generate summary")
parser.add_argument("directory", help="Path to the directory containing the TSV files")
parser.add_argument("output", help="Output TSV file name")
args = parser.parse_args()

files_path = args.directory
output_file = args.output

# Get a list of file names in the directory
files = os.listdir(files_path)

# Define the column names for the desired columns
column_name_of_protid = 'protid'
column_name_of_structure_cluster = 'StruCluster'
column_name_of_scientific_name = 'organism.scientificName'
column_name_of_common_name = 'organism.commonName'
column_name_of_lineage = 'organism.lineage'
column_name_of_sequence_length = 'sequence.length'

# Create a dictionary to map column names to their respective indices
column_indices = {
    column_name_of_protid: None,
    column_name_of_structure_cluster: None,
    column_name_of_scientific_name: None,
    column_name_of_common_name: None,
    column_name_of_lineage: None,
    column_name_of_sequence_length: None
}

# Initialize an empty DataFrame
combined_results_table = pd.DataFrame()

# Iterate over each file
for file in files:
    file_path = os.path.join(files_path, file)
    with open(file_path, 'r') as f:
        # Read the file contents
        file_contents = f.readlines()

        # Extract the header line to get column indices
        header = file_contents[0].strip().split('\t')
        for column_name, index in column_indices.items():
            if column_name in header:
                column_indices[column_name] = header.index(column_name)

        # Extract the desired values from specific columns
        for line in file_contents[1:]:
            columns = line.strip().split('\t')
            TM_v_query_value = None
            reference_value = file[:-4]  # Extract reference value from the file name
            reference_value = reference_value.replace("_aggregated_features_pca_tsne", "")

            for index, column in enumerate(header):
                if re.search(r"TMscore_v_.*", column):
                    TM_v_query_value = columns[index]
                    break

            column_values = {
                'reference': reference_value,
                'protid': columns[column_indices[column_name_of_protid]] if column_indices[column_name_of_protid] is not None else "",
                'structure.cluster': columns[column_indices[column_name_of_structure_cluster]] if column_indices[column_name_of_structure_cluster] is not None else "",
                'sequence.length': columns[column_indices[column_name_of_sequence_length]] if column_indices[column_name_of_sequence_length] is not None else "",
                'organism.scientificName': columns[column_indices[column_name_of_scientific_name]] if column_indices[column_name_of_scientific_name] is not None else "",
                'organism.commonName': columns[column_indices[column_name_of_common_name]] if column_indices[column_name_of_common_name] is not None else "",
                'organism.lineage': columns[column_indices[column_name_of_lineage]] if column_indices[column_name_of_lineage] is not None else "",
                'TM_v_query': TM_v_query_value
            }

            # Append the column values to the DataFrame
            combined_results_table = pd.concat([combined_results_table, pd.DataFrame([column_values])], ignore_index=True)

# Output the final summary TSV file
combined_results_table.to_csv(output_file, sep='\t', index=False)
print(f"Summary TSV file has been generated: {output_file}")
