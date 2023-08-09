#! /usr/bin/env nextflow

// Description
// workflow to profile repeat expansions in FASTA gene sequences

nextflow.enable.dsl=2

params.threads=20
params.outdir=null

log.info """\
PROFILE REPEAT EXPANSIONS IN GENE SEQUENCES
===========================================
input               : $params.input
outdir              : $params.outdir
"""

ch_fasta_query = channel.fromPath("${params.input}/*.{fasta,fa}")
    .map{file -> tuple(file.baseName, file) }


workflow {
    screen_fastas(ch_fasta_query)
    ch_screened_fastas = screen_fastas.out.screened_fasta
    run_utr(ch_screened_fastas)
    ch_utr_fastas = run_utr.out.utr_result.flatten()
    summarize_repeats(ch_utr_fastas.collect())
}

process screen_fastas {
    // screen fastas to remove "N" characters
    tag "${query}_screen"
    publishDir "${params.outdir}/screened", mode: 'copy', pattern: "*.screened.fasta"

    container "python:latest"

    input:
    tuple val(query), path(fasta)

    output:
    tuple val(query), path("*.screened.fasta"), emit: screened_fasta

    script:
    """
    python3 ${baseDir}/bin/screen_fastas.py $fasta
    """
}

process run_utr {
    // run utr
    tag "${query}_utr"
    publishDir "${params.outdir}/utr", mode: 'copy', pattern:"*.utrfasta"

    container "elizabethmcd/utr:localv1" //compiled version of uTR with updated MAX_READS_LENGTH parameter

    errorStrategy 'ignore' // ignore errors that fall outside of length and N issues that should be addressed

    input:
    tuple val(query), path(fasta)

    output:
    path("*.utr.fasta"), emit: utr_result, optional: true

    script:
    """
    uTR -f $fasta -o ${query}.utr.fasta
    """
}

process summarize_repeats {
    tag "summarize_repeats"
    publishDir "${params.outdir}/summary", mode: 'copy', pattern:"*.tsv"

    container "python:latest"

    input:
    path(fasta_files)

    output:
    path("*.tsv"), emit: summary

    script:
    """
    python3 ${baseDir}/bin/parse_utr_fastas.py ${fasta_files.join(' ')} repeat_summaries.tsv
    """
}
