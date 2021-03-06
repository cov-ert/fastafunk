"""
This file is part of Fastafunk (https://github.com/cov-ert/fastafunk).
Copyright 2020 Xiaoyu Yu (xiaoyu.yu@ed.ac.uk) & Rachel Colquhoun (rachel.colquhoun@ed.ac.uk).
"""

from fastafunk.merge import *

def run(options):

    merge_fasta(
        options.in_fasta,
        options.in_metadata,
        options.index_column,
        options.out_metadata,
        options.out_fasta,
        options.log_file,
        options.low_memory
    )