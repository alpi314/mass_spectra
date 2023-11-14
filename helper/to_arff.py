# This script converts a csv file to an arff file
# arff is a file format used by Weka and some other machine learning software

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
parser.add_argument('--shuffle', action='store_true',
                    help='Shuffle the rows')

args = parser.parse_args()

CSV_FILE = args.csv_file
ARFF_FILE = args.arff_file
RELATION = args.relation
SHUFFLE = args.shuffle

if not CSV_FILE.endswith('.csv'):
    raise argparse.ArgumentError('CSV file must be a csv file')

if not ARFF_FILE.endswith('.arff'):
    raise argparse.ArgumentError('ARFF file must be a arff file')

if RELATION is None:
    RELATION = os.path.basename(ARFF_FILE).replace('.arff', '')

df = pd.read_csv(CSV_FILE)

if SHUFFLE:
    df = df.sample(frac=1)

metadata_columns = list(df.columns[df.dtypes == 'object'])
sanitized_metadata_columns = {}
for col in metadata_columns:
    df[col] = df[col].astype(str)
    df[col] = df[col].str.strip().str.replace(',', ';')
    df[col] = df[col].str.strip()
    sanitized_metadata_columns[col] = col.lower().replace(' ', '_')
df = df.rename(columns=sanitized_metadata_columns)

numeric_columns = list(df.columns[df.dtypes != 'object'])
binary = set([0, 1])
for col in numeric_columns:
    vc = df[col].value_counts()
    v = set(vc.keys())
    if v.issubset(binary):
        df[col] = df[col].astype(bool)

arff.dump(ARFF_FILE, df.values, relation=RELATION, names=df.columns)

with open(ARFF_FILE, 'r') as f:
    data = f.read()
    data = data.replace('{True, False}', '{0, 1}')
    data = data.replace(',True', ',1')
    data = data.replace(',False', ',0')

with open(ARFF_FILE, 'w') as f:
    f.write(data)