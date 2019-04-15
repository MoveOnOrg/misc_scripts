import csv
import random
from urllib.parse import parse_qs

from entry_points import run_from_cli

DESCRIPTION = 'Add columns to CSV.'

ARG_DEFINITIONS = {
    'IN': 'Input CSV file.',
    'OUT': 'Output CSV file.',
    'COLUMNS': 'Query string formatted list of name=value additions.',
    'PERCENT': 'Percent of rows to add value (vs. blank). e.g. 0.5 for 50%. Default is 1 (100%).'
}

REQUIRED_ARGS = [
    'IN', 'OUT', 'COLUMNS'
]

def main(args) -> str:

    if not args.PERCENT:
        args.PERCENT = -1

    columns = parse_qs(args.COLUMNS)
    column_names = list(columns.keys())

    with open(args.IN, encoding="ISO-8859-1") as input_file:
        reader = csv.DictReader(input_file)
        headers = reader.fieldnames.copy()
        headers.extend(column_names)

        with open(args.OUT, 'w') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=headers)
            writer.writeheader()

            for row in reader:
                for column in column_names:
                    row[column] = columns[column][0] if (
                        random.random() > float(args.PERCENT)
                    ) else ''
                writer.writerow(row)

    return args.OUT

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
