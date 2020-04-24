from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
import sys
from config import human, mice


if len(sys.argv) <= 1:
    print('Please Specify human or mice')
    exit(1)

config = human if sys.argv[1] == 'human' else mice

PSSM_folder = config['PSSM_folder']
SPD3_folder = config['SPD3_folder']

WINDOW_SIZE = 20
STRUCTURAL_WINDOW_SIZE = 3
LOWEST_VAL = 20

data = {}
final_data = {}


def encoded_to_mapping(encoded):
    global data
    data = {}
    with open(encoded) as fp:
        fp.readline()
        for line in fp:
            row = list(map(str.strip, line.split(',')))
            data[row[1]] = row[3].strip()


def get_bigrams(protein, seq, site_str):
    ind = 0

    X = []
    Y = []
    while ind < len(seq):
        ind = seq.find(site_str, ind)
        if ind == -1:
            break

        ind += 1
        X.append(protein)
        Y.append(int(site_str))

    return [X, Y]


def main(encoded_file, data_folder, ext, output):
    global data

    encoded_to_mapping(encoded_file)
    proteins = [f[0:-9] for f in listdir(data_folder) if isfile(join(data_folder, f)) and f.endswith(ext)]

    X_p = []
    Y_p = []
    X_n = []
    Y_n = []
    for protein in tqdm(proteins):
        mathematical_seq = data[protein].strip()

        # For all Positive Sites
        [a, b] = get_bigrams(protein, mathematical_seq, '1')
        X_p += a
        Y_p += b

        # For all Negative Sites
        [c, d] = get_bigrams(protein, mathematical_seq, '0')
        X_n += c
        Y_n += d

    np.savez(output, X_p, Y_p, X_n, Y_n)


main(config['encoded_file'], config['data_folder'], 'hsb2', config['output'])
