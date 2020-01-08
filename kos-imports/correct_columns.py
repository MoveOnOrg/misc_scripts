import csv
import subprocess
from urllib.parse import parse_qs

from entry_points import run_from_cli

DESCRIPTION = 'Fix column headers for CSV.'

ARG_DEFINITIONS = {
    'IN': 'Input CSV file.',
    'OUT': 'Output CSV file.',
    'CORRECTIONS': 'Query string formatted list of old=new alterations.'
}

REQUIRED_ARGS = [
    'IN', 'OUT', 'CORRECTIONS'
]

def main(args) -> str:
    with open(args.IN, newline='') as input_file:
      reader = csv.reader(input_file)
      headers = next(reader)

    for old, new in list(parse_qs(args.CORRECTIONS).items()):
        if old in headers:
            headers[headers.index(old)] = new[0]

    with open(args.OUT, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=headers)
        writer.writeheader()

    subprocess.run(f'tail -n +2 {args.IN} >> {args.OUT}', shell=True)

    return args.OUT

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
