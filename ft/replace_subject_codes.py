import sys, os, json
from typing import List, Dict


def parse_ics(text: List[str]) -> List[Dict[str, str]]:
    l = []
    for line in text:
        key, value = line.split(':')
        if key == 'BEGIN':
            entry: Dict[str, str] = {}
            continue
        elif key == 'END':
            l.append(entry)
        entry[key] = value
    return l


def main():
    if not (len(sys.argv) == 2 and os.path.isfile(sys.argv[1])):
        print('Run with filename as argument.')
        sys.exit(1)

    fname = sys.argv[1]

    current_dir = os.path.dirname(__file__)
    source_codes = os.path.join(current_dir, 'src/vgs-subject-codes.json')
    with open(source_codes, 'r') as f:
        subject_codes = json.load(f)

    with open(fname, 'r') as infile:
        content = infile.read()

    for code, name in subject_codes.items():
        content = content.replace(code, name)

    with open(fname, 'w') as outfile:
        outfile.write(content)
