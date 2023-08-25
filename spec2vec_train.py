import argparse
import logging
import os
import pickle
import re

import matchms.filtering as ms_filters
from matchms.exporting import save_as_mgf
from matchms.importing import load_from_mgf
from matchms.logging_functions import (set_matchms_logger_level,
                                       set_rdkit_logger_level)
from spec2vec import SpectrumDocument
from spec2vec.model_building import train_new_word2vec_model

# Set logging level to "ERROR" to avoid distracting output during training
set_rdkit_logger_level("rdApp.error")
set_matchms_logger_level("ERROR") # set logging level to "ERROR" to avoid too many messages

# Load all spectra from the any file that ends with ".mgf" in the given directory
def load_from_mgf_files(directory, file_name_ending="", file_extension="mgf"):
    for filename in os.listdir(directory):
        if filename.endswith(f"{file_name_ending}.{file_extension}"):
            print(f"Loading {filename}")
            yield from load_from_mgf(os.path.join(directory, filename))

# Regex to extract information from title
inchi_name = re.compile("InChiKey:\s*([A-Z\-]+).*Name: (.*)")

# Preprocess the metadata
def metadata_processing(s):
    if s.metadata.get("title") and not s.metadata.get("inchikey"):
        matched = inchi_name.findall(s.metadata.get("title"))
        if len(matched) > 0:
            inchikey, name = matched[0]
            s.set("inchikey", inchikey)
            s.set("compound_name", name)
    s = ms_filters.default_filters(s) # general metadata cleaning
    s = ms_filters.repair_inchi_inchikey_smiles(s) # fix wrongly formatted InChI, InChIKey, SMILES
    s = ms_filters.derive_inchi_from_smiles(s) # derive InChI from SMILES
    s = ms_filters.derive_smiles_from_inchi(s) # derive SMILES from InChI
    s = ms_filters.derive_inchikey_from_inchi(s) # derive InChIKey from InChI
    s = ms_filters.harmonize_undefined_smiles(s) # replaces missing SMILES with a common placeholder
    s = ms_filters.harmonize_undefined_inchi(s) # replaces missing InChI with a common placeholder
    s = ms_filters.harmonize_undefined_inchikey(s) # replaces missing InChIKey with a common placeholder
    s = ms_filters.add_precursor_mz(s)
    return s

# Preprocess the peaks
def peak_processing(s):
    s = ms_filters.default_filters(s) # general peak cleaning
    s = ms_filters.normalize_intensities(s) # normalize peak intensities to values between 0 and 1
    s = ms_filters.select_by_intensity(s, intensity_from=0.01) # remove peaks below 0.01 after normalization
    s = ms_filters.select_by_mz(s, mz_from=10, mz_to=1000) # remove peaks outside m/z range 10 to 1000
    return s

# Preprocessing pipeline
def preprocess(s):
    s = metadata_processing(s)
    s = peak_processing(s)
    return convert_to_document(s)

# Preprocess pipeline for the file
def preprocess_file(file_path):
    spectrums = load_from_mgf(file_path)
    return [preprocess(s) for s in spectrums]

# Convert the spectra to SpectrumDocuments
def convert_to_document(s):
    return SpectrumDocument(s, n_decimals=2)

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Train a spec2vec model on a dataset of spectra')

    parser.add_argument('dataset_folder', type=str,
                        help='Path to the dataset folder')
    parser.add_argument('model_save_file', type=str,
                        help='Path to where the model will be saved')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Number of epochs to train the model for (default: 10)')
    parser.add_argument('--file_name_ending', type=str, default="TBDMS_RAW",
                        help='File name ending to filter files by')
    parser.add_argument('--preprocessed_dataset_folder', type=str, default="preprocessed",
                        help='Path to the preprocessed dataset folder')
    parser.add_argument('--use_documents_pickle', action='store_true',
                        help='Use the documents pickle file if it exists')

    args = parser.parse_args()

    # Assign arguments to variables
    DATASET_FOLDER = args.dataset_folder
    MODEL_SAVE_FILE = args.model_save_file
    EPOCHS = args.epochs
    FILE_NAME_ENDING = args.file_name_ending
    PREPROCESSED_DATASET_FOLDER = args.preprocessed_dataset_folder
    USE_DOCUMENTS_PICKLE = args.use_documents_pickle


    # Create the preprocessed dataset folder if it doesn't exist
    os.makedirs(PREPROCESSED_DATASET_FOLDER, exist_ok=True)

    # Load the spectra from the dataset folder and preprocess them
    data_already_preprocessed = os.path.isdir(PREPROCESSED_DATASET_FOLDER) and len(os.listdir(PREPROCESSED_DATASET_FOLDER)) > 0
    if not data_already_preprocessed:
        spectrums = load_from_mgf_files(DATASET_FOLDER, file_name_ending=FILE_NAME_ENDING)
        print("Using data from dataset")

        spectrums = [metadata_processing(s) for s in spectrums]
        spectrums = [peak_processing(s) for s in spectrums]
    elif not USE_DOCUMENTS_PICKLE:
        spectrums = load_from_mgf_files(PREPROCESSED_DATASET_FOLDER, file_name_ending=FILE_NAME_ENDING)
        print("Using data from preprocessed dataset")
        
    if data_already_preprocessed and USE_DOCUMENTS_PICKLE:
        with open(os.path.join(PREPROCESSED_DATASET_FOLDER, "documents.pickle"), "rb") as f:
            documents = pickle.load(f)
        print("Using stored documents")
    else:
        documents = [convert_to_document(s) for s in spectrums if len(s.intensities) > 0]
        print("Using newly created documents")

    # Train the model 
    print(f"Training model with {EPOCHS} epochs on {len(documents)} documents")
    model = train_new_word2vec_model(documents, iterations=EPOCHS, workers=2, progress_logger=True)

    # Save the model
    os.makedirs(os.path.dirname(MODEL_SAVE_FILE), exist_ok=True)
    if not os.path.isfile(MODEL_SAVE_FILE):
        MODEL_SAVE_FILE = os.path.join(MODEL_SAVE_FILE, "spec2vec.model")
    model.save(MODEL_SAVE_FILE)
    print("Model saved to", MODEL_SAVE_FILE)

    # Save the spectra as MGF files
    if not data_already_preprocessed:
        save_as_mgf(spectrums, os.path.join(PREPROCESSED_DATASET_FOLDER, "preprocessed.mgf"))

    # Save documents with pickle
    with open(os.path.join(PREPROCESSED_DATASET_FOLDER, "documents.pickle"), "wb") as f:
        pickle.dump(documents, f)