"""
Name: annotate.py
Author: Rachel Colquhoun
Date: 08 April 2020
Description: Annotates the metadata file with stats calculated from the fasta file.

This file is part of Fastafunk (https://github.com/cov-ert/fastafunk).
Copyright 2020 Xiaoyu Yu (xiaoyu.yu@ed.ac.uk) & Rachel Colquhoun (rachel.colquhoun@ed.ac.uk).
"""

import os
import sys
import re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from fastafunk.utils import *
from fastafunk.stats import *


def annotate(in_fasta, in_metadata, index_column, index_field, out_fasta, out_metadata, header_delimiter,
             add_cov_id, log_file):
    log_handle = get_log_handle(log_file, out_fasta)


    metadata_keys = None
    if in_metadata:
        metadata = load_metadata(in_metadata, None, None)
        metadata, metadata_keys = get_index_column_values(metadata, index_column)

    stats = {"length": [], "missing": [], "gaps": []}
    ids = []
    cov_ids = []

    out_handle = None
    if out_fasta or not out_metadata:
        out_handle = get_out_handle(out_fasta)

    if not in_fasta:
        in_fasta = [""]

    for fasta_file in in_fasta:
        fasta_handle = get_in_handle(fasta_file)
        for record in SeqIO.parse(fasta_handle, "fasta"):
            id = get_index_field_from_header(record, header_delimiter, index_field)
            if metadata_keys is not None and id not in metadata_keys:
                continue
            record_stats = []
            for stat in stats:
                result = get_stat(stat, record)
                record_stats.append("%s=%s" %(stat,str(result)))
                stats[stat].append(result)
            ids.append(id)
            if out_handle:
                if add_cov_id:
                    cov_id = get_cov_id(record)
                    cov_ids.append(cov_id)
                    record_stats.append("id=%s" % cov_id)
                record.description += " " + " ".join(record_stats)
                SeqIO.write(record, out_handle, "fasta-2line")
        close_handle(fasta_handle)

    if out_metadata:
        stats["header"] = ids
        if add_cov_id:
            stats["cov_id"] = cov_ids
        stats_data = pd.DataFrame(stats)
        if in_metadata:
            metadata = add_data(stats_data, metadata)
        else:
            metadata = stats_data
        metadata_handle = get_out_handle(out_metadata)
        metadata.to_csv(out_metadata, index=False)
        close_handle(metadata_handle)

    close_handle(out_handle)
    close_handle(log_handle)



