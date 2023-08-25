# Mass Spectra

## Purpose

Create a pipeline that extracts various molecule fingerprints and their embeddings from mass spectra data.


## Base Usage

Steps to reproduce basic usage of the project.
- Copy and unzip dataset from [data](https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/j3z5bmvmnd-6.zip) to ```dataset/``` folder
- Install conda for enviorment setup
- Create conda environment from ```conda.yml``` file (there might be some unresolved dependancies since they won't be found in conda installer)
- Activate conda environment
- Use ```pip install -r requirements.txt``` to install the remaining dependancies
- Run 
```bash
python spec2vec_train.py ./dataset ./models/tbdms/ --file_name_ending TBDMS_RAW --preprocessed_dataset_folder ./dataset/tbdms_preprocessed/ --use_documents_pickle
```
to train spec2vec model on the TBDMS dataset
- Run 
```bash
python spec2vec_train.py ./dataset ./models/tms/ --file_name_ending TMS_RAW --preprocessed_dataset_folder ./dataset/tms_preprocessed/ --use_documents_pickle
```
to train spec2vec model on the TMS dataset
- Check ```embed.ipynb``` to see how to embed the dataset and adjust model save files if needed
- Run ```embed.ipynb``` to embed the dataset (this will produce 2 fingerprints files and 2 spec2vec embeddings files)
- Checkout other notebooks to see how to use the embeddings and fingerprints and how the pipeline works if you are interested


## Project Structure

- ```temp/``` - contains temporary files that were created on playgrounds as examples
- ```dataset/``` - contains the dataset used in the project avaliable as [data](https://data.mendeley.com/datasets/j3z5bmvmnd/6)
- ```models/``` - contains pretrained models used for examples (NOTE: file endings for some models must not be changed!)
- ```gnps_spectra_libary.mgf``` - contains the raw data used in spec2vec_playground.ipynb avaliable as [data](https://gnps-external.ucsd.edu/gnpslibrary/GNPS-NIH-NATURALPRODUCTSLIBRARY.mgf)
- ```cdk_playground.ipynb``` - contains the code used to test the CDK library
- ```spec2vec_playground.ipynb``` - contains the code used to test the spec2vec library
- ```embed_spectra_playground.ipynb``` - contains the code used to test the embedding of spectra using fingerprints and spec2vec
- ```cdk_inchi_to_fingerprint.py``` - comand line tool that converts inchi to fingerprint
- ```spec2vec_train.py``` - comand line tool that trains spec2vec model
- ```embed.ipynb``` - contains the code used to embed the dataset
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
- Tanimoto similartiy - measure of similarity between two sets of data. It is a metric used to compare the similarity of two sets of data, and is often used in machine learning and data science.

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
- Dataset only includes InChiKey, how can we use it to find the InChi representation of the molecule?

## Future work
- fingerprint feature name
- spec2vec to fingerprint prediction
- pubcem pipeline
- reverse fingerprint to spec2vec

## MACCS fingerprints SMARTS paterns

MACCS fingerprint is a 166bit fingerprint. The official definition of all these keys is not complete, we are following RDKits definitions which are specified [here](https://github.com/rdkit/rdkit-orig/blob/master/rdkit/Chem/MACCSkeys.py).

<style type="text/css" rel="stylesheet">
.comment { color: green; }
.warning {color: yellow}
</style>

- 1:('?',0), <span class="comment"># ISOTOPE</span>
- 2:('[#104,#105,#106,#107,#106,#109,#110,#111,#112]',0), <span class="warning"># atomic num >103 Not complete</span>  
2:('[#104]',0), <span class="comment"> # limit the above definition since the RDKit only accepts up to #104 </span>
- 3:('[#32,#33,#34,#50,#51,#52,#82,#83,#84]',0), <span class="comment"># Group IVa,Va,VIa Rows 4-6 </span> 
- 4:('[Ac,Th,Pa,U,Np,Pu,Am,Cm,Bk,Cf,Es,Fm,Md,No,Lr]',0), <span class="comment"># actinide</span>
- 5:('[Sc,Ti,Y,Zr,Hf]',0), <span class="comment"># Group IIIB,IVB (Sc...)  </span>
- 6:('[La,Ce,Pr,Nd,Pm,Sm,Eu,Gd,Tb,Dy,Ho,Er,Tm,Yb,Lu]',0), <span class="comment"># Lanthanide</span>
- 7:('[V,Cr,Mn,Nb,Mo,Tc,Ta,W,Re]',0), <span class="comment"># Group VB,VIB,VIIB</span>
- 8:('[!#6;!#1]1~*~*~*~1',0), <span class="comment"># QAAA@1</span>
- 9:('[Fe,Co,Ni,Ru,Rh,Pd,Os,Ir,Pt]',0), <span class="comment"># Group VIII (Fe...)</span>
- 10:('[Be,Mg,Ca,Sr,Ba,Ra]',0), <span class="comment"># Group IIa (Alkaline earth)</span>
- 11:('*1~*~*~*~1',0), <span class="comment"># 4M Ring</span>
- 12:('[Cu,Zn,Ag,Cd,Au,Hg]',0), <span class="comment"># Group IB,IIB (Cu..)</span>
- 13:('[#8]~[#7](~[#6])~[#6]',0), <span class="comment"># ON(C)C</span>
- 14:('[#16]-[#16]',0), <span class="comment"># S-S</span>
- 15:('[#8]~[#6](~[#8])~[#8]',0), <span class="comment"># OC(O)O</span>
- 16:('[!#6;!#1]1~*~*~1',0), <span class="comment"># QAA@1</span>
- 17:('[#6]#[#6]',0), <span class="comment"># CTC</span>
- 18:('[#5,#13,#31,#49,#81]',0), <span class="comment"># Group IIIA (B...) </span>
- 19:('*1~*~*~*~*~*~*~1',0), <span class="comment"># 7M Ring</span>
- 20:('[#14]',0), <span class="comment"># Si</span>
- 21:('[#6]=[#6](~[!#6;!#1])~[!#6;!#1]',0), <span class="comment"># C=C(Q)Q</span>
- 22:('*1~*~*~1',0), <span class="comment"># 3M Ring</span>
- 23:('[#7]~[#6](~[#8])~[#8]',0), <span class="comment"># NC(O)O</span>
- 24:('[#7]-[#8]',0), <span class="comment"># N-O</span>
- 25:('[#7]~[#6](~[#7])~[#7]',0), <span class="comment"># NC(N)N</span>
- 26:('[#6]=;@[#6](@*)@*',0), <span class="comment"># C\$=C(\$A)\$A</span>
- 27:('[I]',0), <span class="comment"># I</span>
- 28:('[!#6;!#1]~[CH2]~[!#6;!#1]',0), <span class="comment"># QCH2Q</span>
- 29:('[#15]',0), <span class="comment"># P</span>
- 30:('[#6]~[!#6;!#1](~[#6])(~[#6])~*',0), <span class="comment"># CQ(C)(C)A</span>
- 31:('[!#6;!#1]~[F,Cl,Br,I]',0), <span class="comment"># QX</span>
- 32:('[#6]~[#16]~[#7]',0), <span class="comment"># CSN</span>
- 33:('[#7]~[#16]',0), <span class="comment"># NS</span>
- 34:('[CH2]=*',0), <span class="comment"># CH2=A</span>
- 35:('[Li,Na,K,Rb,Cs,Fr]',0), <span class="comment"># Group IA (Alkali Metal)</span>
- 36:('[#16R]',0), <span class="comment"># S Heterocycle</span>
- 37:('[#7]~[#6](~[#8])~[#7]',0), <span class="comment"># NC(O)N</span>
- 38:('[#7]~[#6](~[#6])~[#7]',0), <span class="comment"># NC(C)N</span>
- 39:('[#8]~[#16](~[#8])~[#8]',0), <span class="comment"># OS(O)O</span>
- 40:('[#16]-[#8]',0), <span class="comment"># S-O</span>
- 41:('[#6]#[#7]',0), <span class="comment"># CTN</span>
- 42:('F',0), <span class="comment"># F</span>
- 43:('[!#6;!#1;!H0]~*~[!#6;!#1;!H0]',0), <span class="comment"># QHAQH</span>
- 44:('?',0), <span class="comment"># OTHER</span>
- 45:('[#6]=[#6]~[#7]',0), <span class="comment"># C=CN</span>
- 46:('Br',0), <span class="comment"># BR</span>
- 47:('[#16]~*~[#7]',0), <span class="comment"># SAN</span>
- 48:('[#8]~[!#6;!#1](~[#8])(~[#8])',0), <span class="comment"># OQ(O)O</span>
- 49:('[!+0]',0), <span class="comment"># CHARGE  </span>
- 50:('[#6]=[#6](~[#6])~[#6]',0), <span class="comment"># C=C(C)C</span>
- 51:('[#6]~[#16]~[#8]',0), <span class="comment"># CSO</span>
- 52:('[#7]~[#7]',0), <span class="comment"># NN</span>
- 53:('[!#6;!#1;!H0]~*~*~*~[!#6;!#1;!H0]',0), <span class="comment"># QHAAAQH</span>
- 54:('[!#6;!#1;!H0]~*~*~[!#6;!#1;!H0]',0), <span class="comment"># QHAAQH</span>
- 55:('[#8]~[#16]~[#8]',0), #OSO
- 56:('[#8]~[#7](~[#8])~[#6]',0), <span class="comment"># ON(O)C</span>
- 57:('[#8R]',0), <span class="comment"># O Heterocycle</span>
- 58:('[!#6;!#1]~[#16]~[!#6;!#1]',0), <span class="comment"># QSQ</span>
- 59:('[#16]!:*:*',0), <span class="comment"># Snot%A%A</span>
- 60:('[#16]=[#8]',0), <span class="comment"># S=O</span>
- 61:('*~[#16](~*)~*',0), <span class="comment"># AS(A)A</span>
- 62:('*@*!@*@*',0), <span class="comment"># A\$!A\$A</span>
- 63:('[#7]=[#8]',0), <span class="comment"># N=O</span>
- 64:('*@*!@[#16]',0), <span class="comment"># A\$A!S</span>
- 65:('c:n',0), <span class="comment"># C%N</span>
- 66:('[#6]~[#6](~[#6])(~[#6])~*',0), <span class="comment"># CC(C)(C)A</span>
- 67:('[!#6;!#1]~[#16]',0), <span class="comment"># QS</span>
- 68:('[!#6;!#1;!H0]~[!#6;!#1;!H0]',0), <span class="comment"># QHQH (&...) SPEC Incomplete</span>
- 69:('[!#6;!#1]~[!#6;!#1;!H0]',0), <span class="comment"># QQH</span>
- 70:('[!#6;!#1]~[#7]~[!#6;!#1]',0), <span class="comment"># QNQ</span>
- 71:('[#7]~[#8]',0), <span class="comment"># NO</span>
- 72:('[#8]~*~*~[#8]',0), <span class="comment"># OAAO</span>
- 73:('[#16]=*',0), <span class="comment"># S=A</span>
- 74:('[CH3]~*~[CH3]',0), <span class="comment"># CH3ACH3</span>
- 75:('*!@[#7]@*',0), <span class="comment"># A!N\$A</span>
- 76:('[#6]=[#6](~*)~*',0), <span class="comment"># C=C(A)A</span>
- 77:('[#7]~*~[#7]',0), <span class="comment"># NAN</span>
- 78:('[#6]=[#7]',0), <span class="comment"># C=N</span>
- 79:('[#7]~*~*~[#7]',0), <span class="comment"># NAAN</span>
- 80:('[#7]~*~*~*~[#7]',0), <span class="comment"># NAAAN</span>
- 81:('[#16]~*(~*)~*',0), <span class="comment"># SA(A)A</span>
- 82:('*~[CH2]~[!#6;!#1;!H0]',0), <span class="comment"># ACH2QH</span>
- 83:('[!#6;!#1]1~*~*~*~*~1',0), <span class="comment"># QAAAA@1</span>
- 84:('[NH2]',0), #NH2
- 85:('[#6]~[#7](~[#6])~[#6]',0), <span class="comment"># CN(C)C</span>
- 86:('[C;H2,H3][!#6;!#1][C;H2,H3]',0), <span class="comment"># CH2QCH2</span>
- 87:('[F,Cl,Br,I]!@*@*',0), <span class="comment"># X!A\$A</span>
- 88:('[#16]',0), <span class="comment"># S</span>
- 89:('[#8]~*~*~*~[#8]',0), <span class="comment"># OAAAO</span>
- 90:('[\$([!#6;!#1;!H0]~*~*~[CH2]~*),\$([!#6;!#1;!H0;R]1@[R]@[R]@[CH2;R]1),\$([!#6;!#1;!H0]~[R]1@[R]@[CH2;R]1)]',0), <span class="comment"># QHAACH2A</span>
- 91:('[\$([!#6;!#1;!H0]~*~*~*~[CH2]~*),\$([!#6;!#1;!H0;R]1@[R]@[R]@[R]@[CH2;R]1),\$([!#6;!#1;!H0]~[R]1@[R]@[R]@[CH2;R]1),\$([!#6;!#1;!H0]~*~[R]1@[R]@[CH2;R]1)]',0), <span class="comment"># QHAAACH2A </span>
- 92:('[#8]~[#6](~[#7])~[#6]',0), <span class="comment"># OC(N)C</span>
- 93:('[!#6;!#1]~[CH3]',0), <span class="comment"># QCH3</span>
- 94:('[!#6;!#1]~[#7]',0), <span class="comment"># QN</span>
- 95:('[#7]~*~*~[#8]',0), <span class="comment"># NAAO</span>
- 96:('*1~*~*~*~*~1',0), <span class="comment"># 5 M ring</span>
- 97:('[#7]~*~*~*~[#8]',0), <span class="comment"># NAAAO</span>
- 98:('[!#6;!#1]1~*~*~*~*~*~1',0), <span class="comment"># QAAAAA@1</span>
- 99:('[#6]=[#6]',0), <span class="comment"># C=C</span>
- 100:('*~[CH2]~[#7]',0), <span class="comment"># ACH2N</span>
- 101:('[\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]1),\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]1),\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]1),\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]1),\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]1),\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]1),\$([R]@1@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]@[R]1)]',0), <span class="comment"># 8M Ring or larger. This only handles up to ring sizes of 14</span>
- 102:('[!#6;!#1]~[#8]',0), <span class="comment"># QO</span>
- 103:('Cl',0), <span class="comment"># CL</span>
- 104:('[!#6;!#1;!H0]~*~[CH2]~*',0), <span class="comment"># QHACH2A</span>
- 105:('*@*(@*)@*',0), <span class="comment"># A\$A(\$A)\$A</span>
- 106:('[!#6;!#1]~*(~[!#6;!#1])~[!#6;!#1]',0), <span class="comment"># QA(Q)Q</span>
- 107:('[F,Cl,Br,I]~*(~*)~*',0), <span class="comment"># XA(A)A</span>
- 108:('[CH3]~*~*~*~[CH2]~*',0), <span class="comment"># CH3AAACH2A</span>
- 109:('*~[CH2]~[#8]',0), <span class="comment"># ACH2O</span>
- 110:('[#7]~[#6]~[#8]',0), <span class="comment"># NCO</span>
- 111:('[#7]~*~[CH2]~*',0), <span class="comment"># NACH2A</span>
- 112:('*~*(~*)(~*)~*',0), <span class="comment"># AA(A)(A)A</span>
- 113:('[#8]!:*:*',0), <span class="comment"># Onot%A%A</span>
- 114:('[CH3]~[CH2]~*',0), <span class="comment"># CH3CH2A</span>
- 115:('[CH3]~*~[CH2]~*',0), <span class="comment"># CH3ACH2A</span>
- 116:('[\$([CH3]~*~*~[CH2]~*),\$([CH3]~*1~*~[CH2]1)]',0), <span class="comment"># CH3AACH2A</span>
- 117:('[#7]~*~[#8]',0), <span class="comment"># NAO</span>
- 118:('[\$(*~[CH2]~[CH2]~*),\$(*1~[CH2]~[CH2]1)]',1), <span class="comment"># ACH2CH2A > 1</span>
- 119:('[#7]=*',0), <span class="comment"># N=A</span>
- 120:('[!#6;R]',1), <span class="comment"># Heterocyclic atom > 1 (&...) Spec Incomplete</span>
- 121:('[#7;R]',0), <span class="comment"># N Heterocycle</span>
- 122:('*~[#7](~*)~*',0), <span class="comment"># AN(A)A</span>
- 123:('[#8]~[#6]~[#8]',0), <span class="comment"># OCO</span>
- 124:('[!#6;!#1]~[!#6;!#1]',0), <span class="comment"># QQ</span>
- 125:('?',0), <span class="comment"># Aromatic Ring > 1</span>
- 126:('*!@[#8]!@*',0), <span class="comment"># A!O!A</span>
- 127:('*@*!@[#8]',1), <span class="comment"># A\$A!O > 1 (&...) Spec Incomplete</span>
- 128:('[\$(*~[CH2]~*~*~*~[CH2]~*),\$([R]1@[CH2;R]@[R]@[R]@[R]@[CH2;R]1),\$(*~[CH2]~[R]1@[R]@[R]@[CH2;R]1),\$(*~[CH2]~*~[R]1@[R]@[CH2;R]1)]',0), <span class="comment"># ACH2AAACH2A</span>
- 129:('[\$(*~[CH2]~*~*~[CH2]~*),\$([R]1@[CH2]@[R]@[R]@[CH2;R]1),\$(*~[CH2]~[R]1@[R]@[CH2;R]1)]',0), <span class="comment"># ACH2AACH2A</span>
- 130:('[!#6;!#1]~[!#6;!#1]',1), <span class="comment"># QQ > 1 (&...)  Spec Incomplete</span>
- 131:('[!#6;!#1;!H0]',1), <span class="comment"># QH > 1</span>
- 132:('[#8]~*~[CH2]~*',0), <span class="comment"># OACH2A</span>
- 133:('*@*!@[#7]',0), <span class="comment"># A\$A!N</span>
- 134:('[F,Cl,Br,I]',0), <span class="comment"># X (HALOGEN)</span>
- 135:('[#7]!:*:*',0), <span class="comment"># Nnot%A%A</span>
- 136:('[#8]=*',1), <span class="comment"># O=A>1 </span>
- 137:('[!C;!c;R]',0), <span class="comment"># Heterocycle</span>
- 138:('[!#6;!#1]~[CH2]~*',1), <span class="comment"># QCH2A>1 (&...) Spec Incomplete</span>
- 139:('[O;!H0]',0), <span class="comment"># OH</span>
- 140:('[#8]',3), <span class="comment"># O > 3 (&...) Spec Incomplete</span>
- 141:('[CH3]',2), <span class="comment"># CH3 > 2  (&...) Spec Incomplete</span>
- 142:('[#7]',1), <span class="comment"># N > 1</span>
- 143:('*@*!@[#8]',0), <span class="comment"># A\$A!O</span>
- 144:('*!:*:*!:*',0), <span class="comment"># Anot%A%Anot%A</span>
- 145:('*1~*~*~*~*~*~1',1), <span class="comment"># 6M ring > 1</span>
- 146:('[#8]',2), <span class="comment"># O > 2</span>
- 147:('[\$(*~[CH2]~[CH2]~*),\$([R]1@[CH2;R]@[CH2;R]1)]',0), <span class="comment"># ACH2CH2A</span>
- 148:('*~[!#6;!#1](~*)~*',0), <span class="comment"># AQ(A)A</span>
- 149:('[C;H3,H4]',1), <span class="comment"># CH3 > 1</span>
- 150:('*!@*@*!@*',0), <span class="comment"># A!A\$A!A</span>
- 151:('[#7;!H0]',0), <span class="comment"># NH</span>
- 152:('[#8]~[#6](~[#6])~[#6]',0), <span class="comment"># OC(C)C</span>
- 153:('[!#6;!#1]~[CH2]~*',0), <span class="comment"># QCH2A</span>
- 154:('[#6]=[#8]',0), <span class="comment"># C=O</span>
- 155:('*!@[CH2]!@*',0), <span class="comment"># A!CH2!A</span>
- 156:('[#7]~*(~*)~*',0), <span class="comment"># NA(A)A</span>
- 157:('[#6]-[#8]',0), <span class="comment"># C-O</span>
- 158:('[#6]-[#7]',0), <span class="comment"># C-N</span>
- 159:('[#8]',1), <span class="comment"># O>1</span>
- 160:('[C;H3,H4]',0), <span class="comment"># CH3</span>
- 161:('[#7]',0), <span class="comment"># N</span>
- 162:('a',0), <span class="comment"># Aromatic</span>
- 163:('*1~*~*~*~*~*~1',0), <span class="comment"># 6M Ring</span>
- 164:('[#8]',0), <span class="comment"># O</span>
- 165:('[R]',0), <span class="comment"># Ring</span>
- 166:('?',0), <span class="comment"># Fragments  FIX: this can't be done in SMARTS</span>