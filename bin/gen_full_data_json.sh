#!/bin/bash

ATD_ORIG_DIR=atd/data

################################################################
# Restore full-data docs from original and meta data, 
# and save them as a json file for each doc.

# main
python src/restore_full_documents.py \
    -i1 $ATD_ORIG_DIR/oversea/with_schedules \
    -i2 atd-mcl-overseas/meta/main/json_per_doc \
    -o atd-mcl-overseas/full/main/json_per_doc

## agreement
python src/restore_full_documents.py \
    -i1 $ATD_ORIG_DIR/oversea/with_schedules \
    -i2 atd-mcl-overseas/meta/agreement/step1_mention_and_step2a_coreference/worker1/json_per_doc \
    -o atd-mcl-overseas/full/agreement/step1_mention_and_step2a_coreference/worker1/json_per_doc 

python src/restore_full_documents.py \
    -i1 $ATD_ORIG_DIR/oversea/with_schedules \
    -i2 atd-mcl-overseas/meta/agreement/step1_mention_and_step2a_coreference/worker2/json_per_doc \
    -o atd-mcl-overseas/full/agreement/step1_mention_and_step2a_coreference/worker2/json_per_doc 

python src/restore_full_documents.py \
    -i1 $ATD_ORIG_DIR/oversea/with_schedules \
    -i2 atd-mcl-overseas/meta/agreement/step2b_link/worker1/json_per_doc \
    -o atd-mcl-overseas/full/agreement/step2b_link/worker1/json_per_doc 

python src/restore_full_documents.py \
    -i1 $ATD_ORIG_DIR/oversea/with_schedules \
    -i2 atd-mcl-overseas/meta/agreement/step2b_link/worker2/json_per_doc \
    -o atd-mcl-overseas/full/agreement/step2b_link/worker2/json_per_doc 
