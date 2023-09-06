# Mass Spectra

## Purpose

Create a pipeline that extracts various molecule fingerprints and their embeddings from mass spectra data. Then train ML models to predict the fingerprint from the embedding.


## Usage

1. Install
- Install Maven (needed for ```scyjava``` python package) ([install guide](https://maven.apache.org/install.html)) and add it to PATH
- Install conda ([install guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))
- Run ```conda env create -f conda.yml --name mass_spectra``` to create conda environment called ```mass_spectra``` (note there might be some non fatal errors for some packages)
- Run ```conda activate mass_spectra``` to activate the environment
- Run ```pip install -r requirements.txt``` to install python packages that might be skipped by conda

2. Setup
- Extract files from [data](https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/j3z5bmvmnd-6.zip) to ```source/dataset/``` folder. (NOTE: the ```source/dataset/``` should directly contain the extracted files without any subfolders).
- Follow the jupyter notebooks in ```pipeline/```  folder. (NOTE: the notebooks should be run in the order they are numbered).
- If you follow the jupyter notebooks the basic pipeline will be executed and all embeddings, Spec2Vec models and ML model should be generated along with evaluation files.

## Project Structure

- ```helper/``` - contains helper functions used by the project
- ```mass_spectra``` - main command line tools also used in jupyter notebooks
- ```pipeline/``` - main pipeline built in jupyter notebooks from embedding to evaluation of trained models
- ```playground/``` - contains jupyter notebooks used for testing and playing around
- ```source/``` - contains the dataset and the generated files (models, spectra, embeddings, etc.)
- ```conda.yml``` - contains the conda environment setup
- ```requirements.txt``` - contains the python packages that are not installed by conda as a fallback

## General Information

1. Articles
- https://jcheminf.biomedcentral.com/articles/10.1186/s13321-022-00636-1
- https://www.sciencedirect.com/science/article/pii/S2352340923002573
- https://jcheminf.biomedcentral.com/articles/10.1186/s13321-017-0220-4
- https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008724


2. Other important external links
- https://cdk.github.io/
- http://cdk.github.io/cdk/latest/docs/api/index.html
- https://github.com/iomega/spec2vec

3. Terminology
- InChikey = International Chemical Identifier key
- TBDMS = Tert-Butyldimethylsilyl chloride
- TMS = Tetramethylsilane
- RAW = raw data, BS = preprocessed data
- GC–MS-EI = Gas Chromatography–Mass Spectrometry (GC–MS) with Cold Electron Ionization (EI)
- Molecular fingerprints = bit string representation
- SMILES = Simplified molecular-input line-entry system
- metabolomics = the large-scale study of small molecules, commonly known as metabolites, within cells, biofluids, tissues or organisms
- metabolites = a substance made or used when the body breaks down food, drugs or chemicals, or its own tissue
- spec2vec = embedding approach that utalizes word2vec to create embeddings from spectral data
- precursor (ion) = ion which is the source of a fragmentation either spontaneous or induced by collisions. Also known as "mother ion".
- m/z = M stands for mass and Z stands for charge number of ions. m/z is the mass-to-charge ratio. (Z is often 1, so m/z is often the same as mass.)
- Tanimoto similartiy = measure of similarity between two sets of data. It is a metric used to compare the similarity of two sets of data, and is often used in machine learning and data science.

4. Chemistry Development Kit (CDK)
- built in Java
- python wrapper: ```scyjava```
- java and python wrapper need [Maven](https://maven.apache.org/install.html)
```python 
from scyjava import config, jimport
config.endpoints.append('org.openscience.cdk:cdk-bundle:2.8')

CircularFingerprinter = jimport('org.openscience.cdk.fingerprint.CircularFingerprinter')
```