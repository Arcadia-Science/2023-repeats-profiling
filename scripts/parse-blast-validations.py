import argparse
from Bio import SeqIO

def fetch_hits(blast_result_file, input_fasta_file, output_folder):
    # Parse the BLAST results
    blast_hits = {}
    with open(blast_result_file, 'r') as blast_file:
        for line in blast_file:
            if line.startswith('#') or not line.strip():
                continue
            fields = line.strip().split('\t')
            query_id = fields[0]
            hit_id = fields[1]
            hit_start = int(fields[8])
            hit_end = int(fields[9])
            # ensure hit_end is the larger of the two, if not then swap them
            if hit_end < hit_start:
                hit_start, hit_end = hit_end, hit_start
            if query_id not in blast_hits:
                blast_hits[query_id] = []
            blast_hits[query_id].append((hit_id, hit_start, hit_end))

    # Parse the input FASTA file as an indexed dictionary (more efficient than SeqIO.todict)
    sequences = SeqIO.index(input_fasta_file, 'fasta')

    # Create individual FASTA files for each hit
    for query_id, hit_info in blast_hits.items():
        for hit_id, hit_start, hit_end in hit_info:
            if hit_id in sequences:
                hit_sequence = str(sequences[hit_id].seq).upper()
                hit_index = hit_sequence[(hit_start-1):(hit_end)]
                hit_record = f">{hit_id}_{hit_start-1}_{hit_end}"
                fasta_record = f"{hit_record}\n{hit_index}"
                output_filename = f"{output_folder}/{hit_id}_{hit_start}_{hit_end}.fasta"
                with open(output_filename, 'w') as output_file:
                    output_file.write(fasta_record)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch hits from BLAST results and create individual FASTA files.")
    parser.add_argument("blast_result_file", help="Path to the BLAST result file")
    parser.add_argument("input_fasta_file", help="Path to the input FASTA file")
    parser.add_argument("output_folder", help="Output folder to save individual FASTA files")

    args = parser.parse_args()

    fetch_hits(args.blast_result_file, args.input_fasta_file, args.output_folder)
