#! /usr/bin/env nextflow

// Description
// workflow to profile repeat expansions in FASTA gene sequences

nextflow.enable.dsl=2

params.threads=4
params.output_dir=null

log.info """\
PROFILE REPEAT EXPANSIONS IN GENE SEQUENCES
===========================================
input               : $params.input
outdir              : $params.outdir
"""

ch_fasta = channel.fromPath(params.input, checkIfExists: true)

workflow {
    run_utr(ch_fasta)

}

process run_utr {
    // run utr
    tag "${ch_fasta}_utr"
    publishDir "${params.outdir}/utr", mode: 'copy', pattern:"*.fasta"

    container "elizabethmcd/utr:v1-release"

    input:
    path(fasta)

    output:
    path("*.utr.fasta"), emit: utr_result

    script:

    """
    uTR -f $fasta -o test.utr.fasta
    """

}
