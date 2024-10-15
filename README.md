# ATD-MCL-Overseas: Overseas Travelogues from Arukikata Travelogue Dataset with Geographic Entity Mention, Coreference, and Link Annotation

## How to Restore the ATD-MCL-Overseas Data

Requirements: Python >= 3.8.0

1. Obtain the Arukikata Travelogue Dataset (ATD) original data (`data.zip`) from the NII IDR site <https://www.nii.ac.jp/dsc/idr/arukikata/>.
1. Decompress `data.zip` and then move `data` directory to under `atd` directory (or create a symbolic link to `data` directory in `atd` directory).
1. Excute `bin/gen_full_data_json.sh`.
    - The restored data will be placed at `atd-mcl-overseas/full/main/json_per_doc/` and `atd-mcl-overseas/full/main/split-*/json`.
    - The data used for calculating inter-annotator aggreement scores will be placed at `atd-mcl-overseas/full/agreement/`.
1. Excute `bin/gen_full_data_tsv.sh`.
    - The restored data will be placed at `atd-mcl-overseas/full/main/link_tsv_per_doc` and `atd-mcl-overseas/full/main/mention_tsv_per_doc`.

## Data Statistics

|Attribute          |Number |
|--                 |--     |
|Document           |     78|
|Section            |  1,309|
|Sentence           |  4,318|
|Chars              |112,591|
|Mention            |  5,116|
|Entity             |  2,263|
|Entity w/ OSM link |  1,361|

This can be obtained by excuting the following command.
- `python src/show_data_statistics.py -i atd-mcl-overseas/full/main/json_per_doc/`.

## Data Format

### JSON Data Format

The JSON data (`atd-mcl-overseas/full/main/split-*/json` and `atd-mcl-overseas/full/main/json_per_doc`) holds full annotation information as follows.

- A document object value is assosiated with a key that represents the  document ID (e.g., `00019`). Each document object has the sets of `sections`, `sentences`, `mentions`, and `entities`.
   ~~~~
    {
      "00711": {
        "sections": {
          "001": {
          ...
          },
        },
        "sentences": {
          "001-01": {
          ...
          },
        },
        "mentions": {
          "M001": {
            ...
          },
        },
        "entities": {
          "E001": {
            ...
          }
        }
      }
    }
    ~~~~
- A section object under `sections` is as follows:
    ~~~~
    "sections": {
      "001": {
        "sentence_ids": [
          "001-01",
          "001-02",
          "001-03",
          "001-04",
          "001-05"
        ]
      },
    ...
    ~~~~
- A sentence object under `sentences` is as follows:
    - A sentence object may have one or more geographic entity mentions.
    - Some sentences with an ID that has a branch number (e.g., "026-01" and "026-02") indicate that a line of text in the original ATD data was split into those multiple sentences.
    ~~~~
    "sentences": {
      "001-01": {
        "section_id": "001",
        "span_in_orig_text": [
          0,
          33
        ],
        "text": "パラオではオプショナルツアーに参加しないとほとんど観光できません。",
        "mention_ids": [
          "M001"
        ]
      },
      ...
      "006-06": {
        "section_id": "006",
        "span_in_orig_text": [
          168,
          173
        ],
        "text": "オススメ!",
        "mention_ids": []
      }
    },
    ~~~~
- A mention object under `mentions` is as follows:
    - A mention object may be associated with an entity.
    ~~~~
    "mentions": {
      "M001": {
        "sentence_id": "001-01",
        "span": [
          0,
          3
        ],
        "text": "パラオ",
        "entity_type": "LOC_NAME",
        "entity_id": "E001"
      },
    ~~~~
- An entity object, which corresponds to a coreference cluster of one or more mentions, under `entities` is as follows:
    - An entity object is associated with one or more mentions.
    - `has_name` indicates whether at least one member mention's entity type is `*_NAME` or not.
    ~~~~
    "entities": {
      "E001": {
        "original_entity_id": "E001",
        "normalized_name": "Republic of Palau;Palau",
        "entity_type_merged": "LOC",
        "has_name": true,
        "has_reference": true,
        "best_ref_type": "OSM",
        "best_ref_url": "https://www.openstreetmap.org/relation/571805",
        "best_ref_query": "Palau",
        "best_ref_area_type": "FOREIGN",
        "member_mention_ids": [
          "M001",
          "M012",
          "M018"
        ]
      },
    ~~~~

### Mention TSV Data Format (tmp)

The mention TSV data (`atd-mcl-overseas/full/main/mention_tsv_per_doc`) holds mention-related annotation information as follows.

- 1st column: document_id
- 2nd column: section_id:sentence_id
- 3rd column: Sentence `text`
- 4th column: Mention information with the following elements. Multiple mentions are enumerated with ";".
  - 1st element: mention_id
  - 2nd element: `span`
  - 3rd element: `entity_type`
  - 4th element: mention `text`
  - 5th element: `entity_id`
  - 6th element: `generic`
  - 7th element: `ref_spec_amb`
  - 8th element: `ref_hie_amb`

Example:
~~~~
00711	002:002-01	日本で化粧品が発売されて有名になった、ミルキーウェイです。	M006,0:2,LOC_NAME,日本,E004,,,;M007,19:26,LOC_NAME,ミルキーウェイ,E005,,,
~~~~
### Link TSV Data Format

The link TSV data (`atd-mcl-overseas/full/main/link_tsv_per_doc`) holds link-related annotation information.
Specifically, entities and their member mentions (except for GENERIC and SPEC_AMB entities/mentions) are listed in TSV rows.
The column with a non-empty `entity_id` value corresponds to an entity, and the column with a non-empty `mention_id` value corresponds to a member mention of the preceding entity column.

Example:

|#document_id|entity_id|mention_id|best_ref_type|best_ref_url|best_ref_query|best_ref_status|best_ref_area_type|second_A_ref_type|second_A_ref_url|second_A_ref_query|second_A_ref_status|second_A_ref_area_type|second_B_ref_type|second_B_ref_url|second_B_ref_query|second_B_ref_status|second_B_ref_area_type|entity_type|span|normalized_name|mention_text|ref_hie_amb|sentence_id|sentence_text|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|00711|E001|-|OSM|https://www.openstreetmap.org/relation/571805|Palau||overseas||||||||||LOC|-|Republic of Palau;Palau|-|-|
|00711|-|E001:M001|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|LOC_NAME|0:3|-|パラオ||001:001-01|パラオではオプショナルツアーに参加しないとほとんど観光できません。|

Notes:
- `mention_id` column values acutally represent "entity_id:mention_id".
- `sentence_id` column values acutally represent "section_id:sentence_id".

## Detailed Data Specification

See `docs/data_specification`.

## License

TBA

## Contact

- Shohei Higashiyama <shohei.higashiyama [at] nict.go.jp>

## Acknowledgements

This study was partly supported by JSPS KAKENHI Grant Number JP22H03648.
The annotation data was constructed by [IR-Advanced Linguistic Technologies Inc.](https://ir-alt.co.jp/)

## Citation

TBA
