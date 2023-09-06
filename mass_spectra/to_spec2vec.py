import argparse

import gensim
import pandas as pd
from spec2vec import Spec2Vec, calc_vector

from mass_spectra.train_spec2vec import preprocess_file

parser = argparse.ArgumentParser(description='Embed spectra using spec2vec model')

parser.add_argument('data_file', type=str,
                    help='Path to the data file')
parser.add_argument('model_file', type=str,
                    help='Path to the model file')
parser.add_argument('output_file', type=str,
                    help='Path to the output file')

args = parser.parse_args()

DATA_FILE = args.data_file
MODEL_FILE = args.model_file
OUTPUT_FILE = args.output_file

if not DATA_FILE.endswith('.mgf'):
    raise argparse.ArgumentError('Data file must be a mgf file')

if not OUTPUT_FILE.endswith('.csv'):
    raise argparse.ArgumentError('Output file must be a csv file')

tms_spectra_documents = preprocess_file(DATA_FILE)

tms_model = gensim.models.Word2Vec.load(MODEL_FILE)
tms_model = Spec2Vec(tms_model)

tms_embedding = []
for spectra in tms_spectra_documents:
    title = spectra.metadata.get('title')
    inchikey = spectra.metadata.get('inchikey')
    embedding = calc_vector(tms_model.model, spectra)
    tms_embedding.append((title, inchikey, *embedding))

tms_columns = ['title', 'inchikey'] + [i for i in range(0, len(tms_embedding[0])-2)]
tms_embedding_df = pd.DataFrame(tms_embedding, columns=tms_columns)

tms_embedding_df.to_csv(OUTPUT_FILE, index=False)