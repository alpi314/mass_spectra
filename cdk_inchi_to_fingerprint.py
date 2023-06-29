import argparse

from chembl_webresource_client.unichem import unichem_client as unichem
from scyjava import config, jimport

config.endpoints.append('org.openscience.cdk:cdk-bundle:2.8')
InChIGeneratorFactory = jimport('org.openscience.cdk.inchi.InChIGeneratorFactory')
InChIToStructure = jimport('org.openscience.cdk.inchi.InChIToStructure')
DefaultChemObjectBuilder = jimport('org.openscience.cdk.DefaultChemObjectBuilder')

InchiGenerator = InChIGeneratorFactory.getInstance()
def inchi_to_atom_container(inchi):
    builderInstance = DefaultChemObjectBuilder.getInstance()
    intostruct = InchiGenerator.getInChIToStructure(inchi, builderInstance)
    return intostruct.getAtomContainer()

def inchikey_to_inchi(inchikey):
    ret = unichem.inchiFromKey(inchikey)
    if len(ret) == 0:
        return None
    return ret[0]['standardinchi']

AVAILABLE_FINGERPRINTS = [
    'AtomPairs2DFingerprinter',
    'CircularFingerprinter',
    'EStateFingerprinter',
    'ExtendedFingerprinter',
    'KlekotaRothFingerprinter',
    'LingoFingerprinter',
    'MACCSFingerprinter',
    'PubchemFingerprinter'
]

FINGERPRINT_ARGS = {
    'PubchemFingerprinter': [DefaultChemObjectBuilder.getInstance()]
}

DEFAULT_PARSER = lambda x: x


def generate_fingerprint(fingerprint_array, inchi_array, fingerprint_parser=DEFAULT_PARSER):
    fingerprints = {}
    for fp in fingerprint_array:
        fingerprints[f'{fp}'] = []

        if fp not in AVAILABLE_FINGERPRINTS:
            raise ValueError(f'Fingerprint type {fp} not available. Options are: {AVAILABLE_FINGERPRINTS}')

        fingerprinter = jimport(f'org.openscience.cdk.fingerprint.{fp}')
        fingerprinter = fingerprinter(*FINGERPRINT_ARGS.get(fp, {}))
        for inchi in inchi_array:
            atom_container = inchi_to_atom_container(f'{inchi}')
            if atom_container.getAtomCount() == 0:
                # retry with inchikey
                atom_container = inchi_to_atom_container(inchikey_to_inchi(inchi))
            if atom_container.getAtomCount() == 0:
                raise ValueError(f'Invalid InChI key: {inchi}')
            fingerprint = fingerprinter.getBitFingerprint(atom_container).asBitSet()
            print(f'{inchi} {fp} {fingerprint_parser(fingerprint)}')

            fingerprints[f'{fp}'].append(fingerprint_parser(fingerprint))
    return fingerprints
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('InChI', type=str,
                        help='InChI key string to convert to fingerprint')
    parser.add_argument('Fingerprint', type=str, 
                        help=f'Fingerprint type to convert to. Options are: {AVAILABLE_FINGERPRINTS}')
    parser.add_argument('--inchi_array', action='store_true',
                        help='Accept array of InChI keys separated by commas')
    parser.add_argument('--fingerprint_array', action='store_true',
                        help='Accept array of fingerprint types separated by commas')
    parser.add_argument('--bit_array', action='store_true',
                        help='Return fingerprint as array of bits instead of BitSet')

    args = parser.parse_args()

    if args.inchi_array:
        inchi_array = args.InChI.split(',')
    else:
        inchi_array = [args.InChI]

    if args.fingerprint_array:
        fingerprint_array = args.Fingerprint.split(',')
    else:
        fingerprint_array = [args.Fingerprint]

    def to_array(bitSet):
        bits = [0] * bitSet.size()
        for i in bitSet.stream().toArray():
            bits[i] = 1
        return bits

    if args.bit_array:
        fingerprint_parser = to_array
    else:
        fingerprint_parser = DEFAULT_PARSER

    try:
        generate_fingerprint(fingerprint_array, inchi_array, fingerprint_parser)
    except ValueError as e:
        parser.error(e)