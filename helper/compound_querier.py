import os
import re
import sys

import pandas as pd
import requests

MAIN_DATA_SOURCE = "./source/compounds/compounds.pkl"
COLUMNS = ['smiles', 'inchi', 'inchi_key']
DATA_FRAME = pd.DataFrame(columns=COLUMNS)
EXPECTED_KEYS = set(DATA_FRAME.columns)

if not os.path.exists(MAIN_DATA_SOURCE):
    os.makedirs(os.path.dirname(MAIN_DATA_SOURCE), exist_ok=True)
    DATA_FRAME.to_pickle(MAIN_DATA_SOURCE)

# Make sure that stored data frame has the same columns as the new data frame
stored_data = pd.read_pickle(MAIN_DATA_SOURCE)
DATA_FRAME = pd.concat([DATA_FRAME, stored_data], ignore_index=True)

host = "https://www.chemspider.com"
query_urls = {
    "inchi_key_to_inchi": "{}/InChI.asmx/InChIKeyToInChI?inchi_key={}",
    "inchi_to_inchi_key": "{}/InChI.asmx/InChIToInChIKey?inchi={}",
    "inchi_to_smiles": "{}/InChI.asmx/InChIToSMILES?inchi={}",
    "smiles_to_inchi": "{}/InChI.asmx/SMILESToInChI?smiles={}",
}
response_value = r"<string .*>(.*)</string>"

def query(url_format, input_value):
    """
    Query the chemspider API
    :param url_format: url format
    :param input_value: input value
    :return: response
    """
    if url_format not in query_urls:
        return None
    
    url = query_urls[url_format].format(host, input_value)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    values = re.findall(response_value, response.text)
    if len(values) == 0:
        print(f"Warning: no value found for {url}")
        return None
    if len(values) > 1:
        print(f"Warning: multiple values found for {url}")
        print(values)
    return values[0]

def validate(data_frame, samples=None, log=False, progress=None):
    if samples is None:
        samples = len(data_frame)

    generator = data_frame.sample(samples).iterrows()
    if progress is not None:
        generator = progress(generator, total=samples)

    invalid = []
    for i, row in generator:
        inchi_key_to_inchi = query("inchi_key_to_inchi", row['inchi_key'])
        inchi_to_inchi_key = query("inchi_to_inchi_key", row['inchi'])
        inchi_to_smiles = query("inchi_to_smiles", row['inchi'])
        smiles_to_inchi_key = query("smiles_to_inchi_key", row['smiles'])

        inchi_key_valid = True
        if inchi_to_inchi_key is not None:
            inchi_key_valid = inchi_key_valid and inchi_to_inchi_key == row['inchi_key']
        if smiles_to_inchi_key is not None:
            inchi_key_valid = inchi_key_valid and smiles_to_inchi_key == row['inchi_key']
        
        inchi_valid = True
        if inchi_key_to_inchi is not None:
            inchi_valid = inchi_valid and inchi_key_to_inchi == row['inchi']
        
        smiles_valid = True
        if inchi_to_smiles is not None:
            smiles_valid = smiles_valid and inchi_to_smiles == row['smiles']
        
        if log:
            if any([not inchi_key_valid, not inchi_valid, not smiles_valid]):
                print(f"Row {i} is invalid")
            if not inchi_key_valid:
                print(f"  Expected inchi key: {row['inchi_key']}; got {inchi_to_inchi_key} and {smiles_to_inchi_key}")
            if not inchi_valid:
                print(f"  Expected inchi: {row['inchi']}; got {inchi_key_to_inchi}")    
            if not smiles_valid:
                print(f"  Expected smiles: {row['smiles']}; got {inchi_to_smiles}")
        invalid.append(row)
    return invalid
        

def get_compound(inchi_key):
    """
    Get compound by inchi key
    :param inchi_key: inchi key
    :return: compound
    """
    global DATA_FRAME
    v = DATA_FRAME.loc[DATA_FRAME['inchi_key'] == inchi_key]
    if len(v) == 0:
        return None
    return v.iloc[0]

def add_compounds(compounds, progress=None, save_every=100):
    global DATA_FRAME
    """
    Add compounds to the data frame
    :param compounds: compounds to add
    :return: None
    """
    if isinstance(compounds, dict):
        compounds = [compounds]
    if isinstance(compounds, pd.DataFrame):
        compounds = compounds.to_dict('records')

    
    existing_values = {c: DATA_FRAME[c].unique() for c in COLUMNS}
    augmented_compounds = []

    generator = enumerate(compounds)
    new = 0
    if progress is not None:
        generator = progress(generator, total=len(compounds))
    for i, c in generator:
        missing_keys = EXPECTED_KEYS - set(c.keys())
        valid_keys = EXPECTED_KEYS.intersection(set(c.keys()))

        # Check if compound already exists
        skip = False
        for vk in valid_keys:
            if c[vk] in existing_values[vk]:
                skip = True
                break
        if skip:
            continue
        new += 1

        missing_keys = sorted(missing_keys, key=lambda x: COLUMNS.index(x))
        valid_keys = sorted(valid_keys, key=lambda x: COLUMNS.index(x))
        for mk in missing_keys:
            for vk in valid_keys:
                result = query(f"{vk}_to_{mk}", c[vk])
                if result is None:
                    continue
                c[mk] = result
                break

        c = {k: c.get(k) for k in EXPECTED_KEYS}
        augmented_compounds.append(c)

        if i % save_every == 0:
            DATA_FRAME = pd.concat([DATA_FRAME, pd.DataFrame(augmented_compounds)], ignore_index=True)
            DATA_FRAME.to_pickle(MAIN_DATA_SOURCE)
            augmented_compounds = []
    print(f"Added {new} new compounds")
    DATA_FRAME = pd.concat([DATA_FRAME, pd.DataFrame(augmented_compounds)], ignore_index=True)
    DATA_FRAME.to_pickle(MAIN_DATA_SOURCE)