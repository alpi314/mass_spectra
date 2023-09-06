import argparse
import os

import arff
import pandas as pd

parser = argparse.ArgumentParser(description='Convert csv to arff')
parser.add_argument('csv_file', type=str,
                    help='Path to the csv file')
parser.add_argument('arff_file', type=str,
                    help='Path to the arff file')
parser.add_argument('--relation', type=str, default=None,
                    help='Relation name (if not specified, will be the arf file name)')

args = parser.parse_args()

CSV_FILE = args.csv_file
ARFF_FILE = args.arff_file
RELATION = args.relation

if not CSV_FILE.endswith('.csv'):
    raise argparse.ArgumentError('CSV file must be a csv file')

if not ARFF_FILE.endswith('.arff'):
    raise argparse.ArgumentError('ARFF file must be a arff file')

if RELATION is None:
    RELATION = os.path.basename(ARFF_FILE).replace('.arff', '')

df = pd.read_csv(CSV_FILE)

metadata_columns = list(df.columns[df.dtypes == 'object'])
sanitized_metadata_columns = {}
for col in metadata_columns:
    df[col] = df[col].astype(str)
    df[col] = df[col].str.strip()
    sanitized_metadata_columns[col] = col.lower().replace(' ', '_')
df = df.rename(columns=sanitized_metadata_columns)

numeric_columns = df.columns[df.dtypes != 'object']
binary = set([0, 1])
for col in numeric_columns:
    vc = df[col].value_counts()
    v = set(vc.keys())
    if v.issubset(binary):
        df[col] = df[col].astype(bool)

arff.dump(ARFF_FILE, df.values, relation=RELATION, names=df.columns)