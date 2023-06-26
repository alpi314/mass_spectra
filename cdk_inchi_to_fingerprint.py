import argparse

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
    fingerprint_parser = lambda x: x

for fp in fingerprint_array:
    if fp not in AVAILABLE_FINGERPRINTS:
        raise parser.error(f'Fingerprint type {fp} not available. Options are: {AVAILABLE_FINGERPRINTS}')

    fingerprinter = jimport(f'org.openscience.cdk.fingerprint.{fp}')
    fingerprinter = fingerprinter(*FINGERPRINT_ARGS.get(fp, {}))
    for inchi in inchi_array:
        atom_container = inchi_to_atom_container(f'InChI={inchi}')
        if atom_container.getAtomCount() == 0:
            raise parser.error(f'Invalid InChI key: {inchi}')
        fingerprint = fingerprinter.getBitFingerprint(atom_container).asBitSet()
        print(f'{inchi} {fp} {fingerprint_parser(fingerprint)}')