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

ch_fasta = channel.fromPath("${params.input}/*.{fasta,fa}")
ch_query = ch_fasta.map { file ->
    file.baseName
}
ch_query.view()

workflow {
    run_utr(ch_fasta, ch_query)

}

process run_utr {
    // run utr
    tag "${query}_utr"
    publishDir "${params.outdir}/utr", mode: 'copy', pattern:"*.fasta"

    container "elizabethmcd/utr:v1-release"

    input:
    path(fasta)
    val(query)

    output:
    path("*.utr.fasta"), emit: utr_result

    script:

    """
    uTR -f $fasta -o ${query}.utr.fasta
    """

}
