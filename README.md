# Mass Spectra

## Purpose

Create a pipeline that extracts various molecule fingerprints and their embeddings from mass spectra data.


## Project Structure

- ```temp/``` - contains temporary files that were created on playgrounds as examples
- ```dataset/``` - contains the dataset used in the project avaliable as [data](https://data.mendeley.com/datasets/j3z5bmvmnd/6)
- ```models/``` - contains pretrained models used for examples (NOTE: file endings for some models must not be changed!)
- ```matchms/``` - modified file from [matchms](https://github.com/matchms/matchms), saved as reference if pull request is not accepted
- ```gnps_spectra_libary.mgf``` - contains the raw data used in spec2vec_playground.ipynb avaliable as [data](https://gnps-external.ucsd.edu/gnpslibrary/GNPS-NIH-NATURALPRODUCTSLIBRARY.mgf)
- ```cdk_playground.ipynb``` - contains the code used to test the CDK library
- ```spec2vec_playground.ipynb``` - contains the code used to test the spec2vec library
- ```inchi_to_fingerprint.py``` - comand line tool that converts inchi to fingerprint
- ```requirements.txt``` - contains the required python libraries
- ```requirements_conda.txt``` - contains the conda environment libraries

## General Information

Articles:
- https://jcheminf.biomedcentral.com/articles/10.1186/s13321-022-00636-1
- https://www.sciencedirect.com/science/article/pii/S2352340923002573
- https://jcheminf.biomedcentral.com/articles/10.1186/s13321-017-0220-4
- https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008724

Data:
- https://data.mendeley.com/datasets/j3z5bmvmnd/6
- Avaliable in dataset folder

Software:
- https://cdk.github.io/
- CDK http://cdk.github.io/cdk/latest/docs/api/index.html
- https://github.com/iomega/spec2vec

Terminology:
- InChikey: https://en.wikipedia.org/wiki/International_Chemical_Identifier
- TBDMS = Tert-Butyldimethylsilyl chloride
- TMS = Tetramethylsilane
- RAW = raw data, BS = preprocessed data
- Gas Chromatography–Mass Spectrometry (GC–MS) with Cold Electron Ionization (EI)
- Molecular fingerprints = bit string representation
- SMILES = Simplified molecular-input line-entry system
- metabolomics = the large-scale study of small molecules, commonly known as metabolites, within cells, biofluids, tissues or organisms
- metabolites = a substance made or used when the body breaks down food, drugs or chemicals, or its own tissue
- spec2vec = embedding approach that utalizes word2vec to create embeddings from spectral data
- precursor (ion) - ion which is the source of a fragmentation either spontaneous or induced by collisions. Also known as "mother ion".
- m/z - M stands for mass and Z stands for charge number of ions. m/z is the mass-to-charge ratio. (Z is often 1, so m/z is often the same as mass.)
- Tanimoto - similarity is a measure of similarity between two sets of data. It is a metric used to compare the similarity of two sets of data, and is often used in machine learning and data science.

Usage of CDK:
- CDK is built in Java
- We can use it in python with ```scyjava```
- We need to install Java and Maven to use ```scyjava```
- We can use ```scyjava``` to import classes from CDK
- example: 
```python 
from scyjava import config, jimport
config.endpoints.append('org.openscience.cdk:cdk-bundle:2.8')

CircularFingerprinter = jimport('org.openscience.cdk.fingerprint.CircularFingerprinter')
```

Fingerprint selection:
- https://mattermodeling.stackexchange.com/questions/1175/what-are-the-best-fingerprints-to-characterize-molecules (recommended MACCS, Circular, )

Questions and considerations:
- Dataset does not include the precursor ion mass, how can we find it, is it important?
