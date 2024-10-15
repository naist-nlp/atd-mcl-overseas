import json
import sys
import unicodedata


SPACES    = ''.join([' ', chr(0x2028), '　'])
CTRL_CHR1 = '\x7f'


def load_json(
        input_path: str,
) -> dict:

    with open(input_path) as f:
        print(f'[Info] Read: {input_path}', file=sys.stderr)
        data = json.load(f)
    return data


def write_as_json(
        data: dict,
        output_path: str,
) -> None:

    with open(output_path, 'w') as fw:
        json.dump(data, fw, ensure_ascii=False, indent=2)
    print(f'[Info] Saved: {output_path}', file=sys.stderr)


def load_id_list(
        path: str,
) -> list:

    id_list = []

    with open(path) as f:
        for line in f:
            id_str = line.rstrip('\n').split('\t')[0]
            id_list.append(id_str)

    return id_list


def normalize_text(
        text: str,
) -> str:

    return (unicodedata.normalize('NFKC', text)
            .replace(CTRL_CHR1, ' ').replace(' ', '　').strip(SPACES))


def replace_control_chars(
        text: str,
) -> str:

    return text.replace(CTRL_CHR1, '　')
