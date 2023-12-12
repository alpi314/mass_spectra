import pandas as pd
from chembl_webresource_client.unichem import unichem_client as unichem
from scyjava import config, jimport

config.endpoints.append('org.openscience.cdk:cdk-bundle:2.8')
InChIGeneratorFactory = jimport('org.openscience.cdk.inchi.InChIGeneratorFactory')
InChIToStructure = jimport('org.openscience.cdk.inchi.InChIToStructure')
DefaultChemObjectBuilder = jimport('org.openscience.cdk.DefaultChemObjectBuilder')


def compound_info(inchi):
    factory = InChIGeneratorFactory()
    intostruct = factory.getInChIToStructure(inchi, DefaultChemObjectBuilder.getInstance())
    atom_container = intostruct.getAtomContainer()
    # ger molecule name from inchi
    name = atom_container.getProperty('PUBCHEM_IUPAC_NAME')