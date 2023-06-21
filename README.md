# Mass Spectra

## Purpose

Create a pipeline that extracts various molecule fingerprints and their embeddings from mass spectra data.


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

Notes:
- InChikey: https://en.wikipedia.org/wiki/International_Chemical_Identifier
- TBDMS = Tert-Butyldimethylsilyl chloride
- TMS = Tetramethylsilane
- RAW = raw data, BS = preprocessed data
- Gas Chromatography–Mass Spectrometry (GC–MS) with Cold Electron Ionization (EI)
- Molecular fingerprints = bit string representation
- SMILES = Simplified molecular-input line-entry system

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
