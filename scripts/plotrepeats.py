
import os

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sbn
import numpy as np
import arcadia_pycolor as apc
apc.mpl_setup()

def load_data(input_folder):

    #load the variables output from analyzecountedAAs script
    gene = input_folder.split('/')[-1]

    combo_df = pd.read_csv(os.path.join(input_folder,"repeatswithhomology.csv"))
    max_human_repeats = pd.read_csv(os.path.join(input_folder,"max_human_repeats.csv"))

    AA_reps = pd.read_csv(os.path.join(input_folder,"pathologic_AA_repeats.csv"))
    hit_species = pd.read_csv(os.path.join(input_folder,"hit_species.csv"))
    repeatAA = hit_species["Letter"].loc[0]

    return gene,combo_df,hit_species, max_human_repeats, repeatAA, AA_reps

def allAA_Lengths(folder,combo_df,gene,repeatAA,max_human_repeats):
    #histogram the length of homolog repeat lengths relative to the human reference (if it has a repeat)

    #define bin sizes
    binwidth =1
    maxrep = int(combo_df["Length"].max())
    minrep = int(combo_df["Length"].min())

    bins=range(minrep, maxrep + binwidth, binwidth)

    #histogram for each amino acid the length of homlog repeats
    g = combo_df.hist("Length",by= "Letter",figsize =[15, 15], bins=bins, color="arcadia:marineblue")
    plt.suptitle(gene + " homolog repetetive amino acid sequences ", size=20)

    #for each subplot change the y-axis to log, set a y-range, and makr the human reference with a line
    for axis in g.ravel():
        axis.set_yscale('log')
        axis.set_ylim([0.1,1E3])
        axis.set_ylabel("# of occurences", size=12)
        axis.set_xlabel("length of repeat", size=12)
        this_AA = axis.get_title()
        if this_AA == repeatAA:
            axis.set_facecolor("arcadia:Dawn")

        try:
            human_length = max_human_repeats[max_human_repeats["Letter"]==axis.get_title()]["Length"].values
            axis.axvline(x =human_length[0]+0.5, color = 'arcadia:rose', label = 'human reference')
            axis.legend(frameon=False)
        except:
            None

    plt.savefig(os.path.join(folder,'homolog_allAAs_repeat_lengths.png'), format='png', dpi=1200)

def expansionAA_lengths(folder,AA_reps,gene,repeatAA,max_human_repeats):
    ## make a histogram just of repeat lengths for the pathology-associated amino acid

    binwidth =1
    maxrep = int(AA_reps["Length"].max())
    minrep = int(AA_reps["Length"].min())
    bins=range(minrep, maxrep + binwidth, binwidth)

    plt.figure()
    axes = plt.hist(AA_reps["Length"], bins=bins,color="arcadia:marineblue")
    try:
        human_length = max_human_repeats[max_human_repeats["Letter"]==repeatAA]["Length"].values
        plt.axvline(human_length[0]+0.5, color = 'arcadia:rose', label = 'human reference')
    except:
        None
    plt.yscale("log")
    plt.ylabel("# of occurences", size=12)
    plt.xlabel("length of repeat", size=12)
    plt.title(gene + " distribution of '" + repeatAA + "' repeats", size=16)
    plt.legend(loc=0, frameon = False)

    plt.savefig(os.path.join(folder,'homolog_expansionAA_repeat_lengths.png'), format='png', dpi=1200)

def expansionAA_lengthvsIdentity(output_folder,AA_reps,gene,repeatAA,max_human_repeats):
    #scatter plot the repeat length of homolgs versus sequence/structural identity with the human protein
    fig, ax = plt.subplots(figsize=(8,6))

    #filter so each species only has one hit per dRE
    AA_reps = AA_reps.sort_values('Length', ascending=False).drop_duplicates(subset = ['Scientific Name']).sort_index()

    try:
        AA_reps['Per. Ident'].combine_first(AA_reps['TM_v_query']*100) #combine with TM score if using structural similarity data too
    except: None

    sbn.scatterplot( data=AA_reps, x = "Per. Ident", y = "Length",
                     hue="ToLdiv", palette= 'arcadia:Accent')

    #if the human reference has a repeat mark that length with a horizontal line
    human_length = max_human_repeats[max_human_repeats["Letter"]==repeatAA]["Length"].values
    try:
        ax.axhline(y=human_length[0], color = "arcadia:rose" , label="human reference")
    except: None

    #label and save
    ax.set_xlabel(f"% sequence identity or TM score, with human " + gene, size=12)
    ax.set_ylabel("length of '" + repeatAA + "' repeats", size=12)
    plt.title(gene + " homolog '" + repeatAA + "' repeat length vs identity", size=16)

    plt.savefig(os.path.join(output_folder,'homolog_repeatAA_vsidentity.png'), format='png', dpi=1200)

def plot_allDRE_pathologicalAA(all_AA_reps, y_metric = "Human Normal Max Delta"):
    #violin plot the homolog lengths for each gene relative to some shared metric (e.g. length relative to the human reference,
    # length relative to human normal max etc.)
    fig, ax = plt.subplots(figsize=(8,6))

    sbn.violinplot(data = all_AA_reps.sort_values(by="gene"), x="gene", y= y_metric, scale="width", inner="box")
    # to use arcadia color palette add palette="arcadia:AllOrdered"
    ax.axhline(y=0, color = "arcadia:Seaweed" , linestyle = "dashed", label="human reference")

    plt.xticks(rotation=90)
    plt.ylabel('repeat length relative to human',fontsize = 12)
    plt.xlabel('gene',fontsize = 12)

def plot_analyzed_AAcounts(input_dir,close_logical=True):
    #make plots for each homolog folder with analyzed repeat counts
    for gene_folder in os.scandir(input_dir):
        if not gene_folder.is_dir(): continue

        gene_folder = gene_folder.path
        gene,combo_df,hit_species, max_human_repeats, repeatAA, AA_reps = load_data(gene_folder)
        allAA_Lengths(gene_folder,combo_df,gene,repeatAA,max_human_repeats)
        if close_logical: plt.close()
        expansionAA_lengths(gene_folder,AA_reps,gene,repeatAA,max_human_repeats)
        if close_logical: plt.close()
        expansionAA_lengthvsIdentity(gene_folder,AA_reps,gene,repeatAA,max_human_repeats)
        if close_logical: plt.close()
