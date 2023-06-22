#! /usr/bin/env nextflow

// Description
// workflow to profile repeat expansions in FASTA gene sequences

nextflow.enable.dsl=2

params.threads=4
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
    run_utr(ch_fasta_query)
    ch_utr_fastas = run_utr.out.utr_result.flatten()
    summarize_repeats(ch_utr_fastas.collect())
}

process run_utr {
    // run utr
    tag "${query}_utr"
    publishDir "${params.outdir}/utr", mode: 'copy', pattern:"*.fasta"

    container "elizabethmcd/utr:v1-release"

    input:
    tuple val(query), path(fasta)

    output:
    path("*.utr.fasta"), emit: utr_result

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
