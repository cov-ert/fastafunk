"""
Name: remove.py
Author: Xiaoyu Yu
Date: 07 April 2020
Description: Remove sequences from fasta file with matching sequence names within the metadata file.

Log file will flag all sequences removed from fasta file based on matches on metadata file.

This file is part of Fastafunk (https://github.com/cov-ert/fastafunk).
Copyright 2020 Xiaoyu Yu (xiaoyu.yu@ed.ac.uk) & Rachel Colquhoun (rachel.colquhoun@ed.ac.uk).
"""

import csv
from Bio import SeqIO

from fastafunk.utils import *

def remove_fasta(in_fasta, in_metadata, out_fasta, log_file):
    """
    Remove sequences from fasta file with matching sequence names within the metadata file

    :param in_fasta: Fasta file with sequences that needs to be filtered according to metadata file. (Required)
    :param in_metadata: Matching metadata file with same naming convention as fasta file. Contains sequences that the
    user wants to remove from the fasta file. Metadata file must be in .csv format (Required)
    :param out_fasta: Output fasta file filtered sequences removed based on metadata file
    (Default: remove_by_metadata.fasta). (Optional)
    :param log_file: Output log file (Default: stdout). (Optional)

    :return:
    """
    if not in_fasta:
        in_fasta = [""]
    metadata_dictionary = metadata_to_dict(in_metadata)

    out_handle = get_out_handle(out_fasta)
    log_handle = get_log_handle(log_file, out_fasta)

    for fasta_file in in_fasta:
        fasta_handle = get_in_handle(fasta_file)
        for record in SeqIO.parse(fasta_handle, "fasta"):
            if record.id not in metadata_dictionary.keys():
                SeqIO.write(record, out_handle, "fasta-2line")
            else:
                print("Sequence " + record.id + " removed due to match to metadata", file=log_handle)
        close_handle(fasta_handle)

    close_handle(out_handle)
    close_handle(log_handle)