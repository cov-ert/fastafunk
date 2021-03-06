"""
This file is part of Fastafunk (https://github.com/cov-ert/fastafunk).
Copyright 2020 Xiaoyu Yu (xiaoyu.yu@ed.ac.uk) & Rachel Colquhoun (rachel.colquhoun@ed.ac.uk).
"""

from fastafunk.extract import *

def run(options):

    extract_fasta(
        options.in_fasta,
        options.in_metadata,
        options.in_tree,
        options.out_fasta,
        options.reject_fasta,
        options.low_memory,
        options.log_file
    )
