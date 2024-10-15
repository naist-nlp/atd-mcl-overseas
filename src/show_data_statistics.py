import argparse
from collections import Counter
import json
import os
import sys

from util import load_json


SECS          = 'sections'
SENS          = 'sentences'
MENS          = 'mentions'
ENTS          = 'entities'

SEC_ID        = 'section_id'
SEN_ID        = 'sentence_id'
MEN_IDS       = 'mention_ids'
ENT_ID        = 'entity_id'
MEM_MEN_IDS   = 'member_mention_ids'

TXT           = 'text'
ENT_TYPE      = 'entity_type'
HAS_REF       = "has_reference"
BEST_REF_TYPE = "best_ref_type"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_dirs', '-i',
        type=str,
        required=True,
    )
    args = parser.parse_args()

    data = {}
    for input_dir in args.input_dirs.split(','):
        for file_name in os.listdir(input_dir):
            if not file_name.endswith('.json'):
                continue

            input_path = os.path.join(input_dir, file_name)
            data_orig = load_json(input_path)
            for doc_id, doc in data_orig.items():
                data[doc_id] = data_orig[doc_id]

    # data statistics
    counter = Counter()
    key2sets = {'num_mentions': set()}

    for doc_id, doc in data.items():
        counter['num_documents'] += 1
        if SECS in doc:
            counter['num_sections'] += len(doc[SECS])

        if SENS in doc:
            counter['num_sentences'] += len(doc[SENS])

            for sen_id, sen in doc[SENS].items():
                sen_text = sen[TXT]
                counter['num_chars'] += len(sen_text)

        if MENS in doc:
            counter['num_mentions'] += len(doc[MENS])

            for men_id, men in doc[MENS].items():
                key2sets['num_mentions'].add(men[TXT])

                if ENT_TYPE in men:
                    key = f'num_mentions:entity_type={men[ENT_TYPE]}'
                    counter[key] += 1
                    if not key in key2sets:
                        key2sets[key] = set()
                    key2sets[key].add(men[TXT])

        if ENTS in doc:
            counter['num_entities'] += len(doc[ENTS])

            for ent_id, ent in doc[ENTS].items():
                if HAS_REF in ent and ent[HAS_REF]:
                    counter['num_entities:has_ref'] += 1
                    counter[f'num_entities:ref_type={ent[BEST_REF_TYPE]}'] += 1

                has_name = False
                for men_id in ent[MEM_MEN_IDS]:
                    men = doc[MENS][men_id]
                    if men[ENT_TYPE].endswith('NAME'):
                        has_name = True

                if has_name:
                    counter['num_entities:has_name'] += 1

    print('\nData statistics -- Total (Unique):')
    main_keys = ['num_documents', 'num_sections', 'num_sentences', 'num_chars', 
                 'num_mentions', 'num_entities']
    for key in main_keys:
        val = counter[key]
        if key in key2sets:
            val2 = len(key2sets[key])
            print(f'{key}\t{val}\t({val2})')
        else:
            print(f'{key}\t{val}')
        
    for key, val in sorted(counter.items()):
        if not key in main_keys:
            if key in key2sets:
                val2 = len(key2sets[key])
                print(f'{key}\t{val}\t({val2})')
            else:
                print(f'{key}\t{val}')


if __name__ == '__main__':
    main()
