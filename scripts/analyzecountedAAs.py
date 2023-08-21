
import os
import pandas as pd
import numpy as np
from scipy.stats import zscore

#points to csv of all homologs that contains a column with the header "gene"
def analyzecountedAAs(input_dir = "../results/countedAAs",
                       repeat_location_path = "../inputs/geneID_Region_andPathogenicLength.csv",
                       homology_file_path = "../results/homology_results/dREhomologs_MR20230710.csv",
                       output_path = "../results/analyzed_AAcounts",
                       nrepeat_filt = 2):
    ''' analyze_countedAAs: takes a folder of output .csv files from find_consecutive_repeated_letters,
        and analyzes it if the repeat expansion in that gene is in a coding region. Alaysis consists of
        filtering, merging with the homology results (e.g. BLAST), and comparing the repeat length for the
        disease-causing amino acid to the human reference to identify species with repetitive amino acids
        equal or greather than the human

        usage:  analyze_countedAAs -input_dir -repeat_location_path -homology_file_path -output_path
        -nrepeat_filt

        outputs:
        -repeats_with_homology.csv: the combined dataframe of repeat lengths with homology data
        -max_human_repeats.csv: the max repetitive amino acid length in the human reference
        -hit_species.csv: a list of species, with homology and max repetitive amino acid length, that
        matches or exceeds the max length found in the human reference
        '''


    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    for file in os.listdir(input_dir):

        if ".DS_Store" in file: continue #ignoring .DS_store

        #find genes where a coding expansion causes disease, and which amino acid it is:
        gene = file.split('/')[-1].split('.')[0]
        repeat_location_df = pd.read_csv(repeat_location_path)
        this_region = str(repeat_location_df[repeat_location_df["Locus ID"] == gene]["GeneRegion"])

        if not "coding" in this_region or "other" in this_region: continue
        this_region = this_region.split(":")[1]

        if "alanine" in this_region: repeatAA = "A"
        if "glutamine" in this_region: repeatAA = "Q"
        if "glycine" in this_region: repeatAA = "G"
        if "serine" in this_region: repeatAA = "S"
        if "aspartic" in this_region: repeatAA = "D"

        try: normal_max = repeat_location_df[repeat_location_df["Locus ID"] == gene]["NormalMax"].values[0]
        except: normal_max = np.NaN
        try: pathogenic_min = repeat_location_df[repeat_location_df["Locus ID"] == gene]["PathogenicMin"].values[0]
        except: pathogenic_min = np.NaN

        #fix some mistakes in normal max and pathogenic min
        if gene == "COMP":
            normal_max = 5
        if gene == "PABPN1":
            normal_max = 10
            pathogenic_min =11

        #make a new folder
        output_folder = os.path.join(output_path,gene)
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)

        #load repeat counts for this gene and filter
        repeats = pd.read_csv(os.path.join(input_dir,file))
        repeats = repeats.drop(columns=["Unnamed: 0"])
        repeats["Accession"] = repeats["Accession"].str.split('.fa').str[0]

        #filter repeats
        filtered_repeats = repeats[repeats["Letter"].str.contains("N|X") == False]
        filtered_repeats = filtered_repeats[filtered_repeats["Length"]> nrepeat_filt]

        #load homology results
        homolog_df = pd.read_csv(homology_file_path)

        #make sure there are no obvious duplicates
        filtered_repeats.drop_duplicates(inplace=True)
        filtered_repeats.reset_index(inplace=True,drop=True)
        homolog_df.drop_duplicates(inplace=True)
        homolog_df.reset_index(inplace=True,drop=True)

        #merge dataframes
        combo_df = pd.merge(homolog_df,filtered_repeats, on="Accession")
        combo_df = combo_df.loc[:, ~combo_df.columns.str.contains('^Unnamed')]
        combo_df = combo_df[combo_df["gene"] == gene]
        combo_df.reset_index(drop=True,inplace=True)

        #find the longest repeats in this gene from the human reference
        human_repeats = combo_df[combo_df["Scientific Name"].str.contains("Homo sapiens",na=False)]
        human_repeats = human_repeats[human_repeats["database"]=='refseq']
        if ~human_repeats.empty: #if there was a human refseq homolog, use it
            max_human_repeats = human_repeats.groupby(["Letter"])['Length'].max()

        #find species with amino acid stretches as long or longer than humans
        AA_reps = combo_df[combo_df["Letter"].str.contains(repeatAA)].reset_index(drop=True)
        AA_reps["Length Zscore"] = AA_reps["Length"].transform(zscore)

        try: AA_reps["Human Reference Delta"]= AA_reps["Length"]-max_human_repeats[repeatAA]
        except: AA_reps["Human Reference Delta"]= np.NAN

        try: AA_reps["Human Normal Max Delta"]= AA_reps["Length"]-int(normal_max)
        except: AA_reps["Human Normal Max Delta"]= np.NAN

        try: AA_reps["Human Pathogenic Min Delta"]= AA_reps["Length"]-int(pathogenic_min)
        except: AA_reps["Human Pathogenic Min Delta"]== np.NAN

        #Drop humans and synthetic constructs from results
        AA_reps = AA_reps[AA_reps["Scientific Name"].str.contains("synthetic construct|Homo sapiens")==False]

        try:
            #this fails if no repeats can be found in the human reference (namely for JPH3)
            hit_species = AA_reps[AA_reps["Length"]>=max_human_repeats[repeatAA]]
        except:
            hit_species = AA_reps

        AA_reps = AA_reps.sort_values("Length",ascending=False).reset_index(drop=True)
        hit_species = hit_species.sort_values("Length",ascending=False).reset_index(drop=True)

        try:
            all_hit_species = pd.concat([all_hit_species, hit_species], ignore_index=True, axis=0)
            all_AA_reps = pd.concat([all_AA_reps, AA_reps], ignore_index=True, axis=0)

        except:
            all_hit_species = hit_species
            all_AA_reps = AA_reps

        #save dataframes
        combo_df.to_csv(os.path.join(output_folder,"repeatswithhomology.csv"))
        max_human_repeats.to_csv(os.path.join(output_folder,"max_human_repeats.csv"))
        hit_species.to_csv(os.path.join(output_folder,"hit_species.csv"))
        AA_reps.to_csv(os.path.join(output_folder,"pathologic_AA_repeats.csv"))

    all_hit_species.to_csv(os.path.join(output_path,"all_hit_species.csv"))
    all_AA_reps.to_csv(os.path.join(output_path,"all_pathologic_AA_repeats.csv"))
