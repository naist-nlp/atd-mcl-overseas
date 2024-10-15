#!/bin/bash

ATD_ORIG_DIR=atd/data

################################################################
# Convert json files to tsv files

# main
python src/convert_json_to_tsv.py \
       -i atd-mcl-overseas/full/main/json_per_doc \
       -o1 atd-mcl-overseas/full/main/mention_tsv_per_doc \
       -o2 atd-mcl-overseas/full/main/link_tsv_per_doc
