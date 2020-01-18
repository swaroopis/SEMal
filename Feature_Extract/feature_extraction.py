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


def get_PSSM(protein, protein_sz, ind):
    with open(PSSM_folder + protein + '.seq.pssm') as fp:
        # Read 3 lines for the top padding lines
        fp.readline()
        fp.readline()
        fp.readline()

        PSSMs = fp.readlines()
        PSSM_list = []

        for val in range(ind - WINDOW_SIZE, ind + WINDOW_SIZE + 1):
            now = val
            if val < 0 or val >= protein_sz:
                distance = ind - val
                now = ind + distance

            row = list(map(int, PSSMs[now].strip().split()[2:2 + 20]))
            PSSM_list.append(row)

        return PSSM_list


def get_profile_bigram(PSSM, flatten = False):
    B = [[0 for x in range(20)] for y in range(20)]
    for p in range(20):
        for q in range(20):
            now = 0
            for k in range(0, WINDOW_SIZE * 2):
                now += PSSM[k][p] * PSSM[k + 1][q]
            B[p][q] = now

    return np.asarray(B).flatten() if flatten else B


def get_structural_info(protein, protein_sz, ind, flatten=False):
    with open(SPD3_folder + protein + '.seq.spd3') as fp:
        # Read 3 lines for the top padding lines
        fp.readline()

        SSpres = fp.readlines()
        SSpre_list = []

        for val in range(ind - STRUCTURAL_WINDOW_SIZE, ind + STRUCTURAL_WINDOW_SIZE + 1):
            now = val
            if val < 0 or val >= protein_sz:
                distance = ind - val
                now = ind + distance

            row = list(map(float, SSpres[now].strip().split()[3:]))
            SSpre_list.append(row)

        return np.asarray(SSpre_list).flatten() if flatten else SSpre_list


def get_bigrams(protein, seq, site_str):
    ind = 0

    X = []
    Y = []
    while ind < len(seq):
        ind = seq.find(site_str, ind)
        if ind == -1:
            break

        PSSM = get_PSSM(protein, len(seq), ind)
        PSSM_bigram = get_profile_bigram(PSSM, True)  # 20 x 20
        SPpre = get_structural_info(protein, len(seq), ind, True)
        ind += 1

        combined = np.concatenate((PSSM_bigram, SPpre))

        X.append(combined)
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

    np.savez('../data/{}.npz'.format(output), X_p, Y_p, X_n, Y_n)


main(config['encoded_file'], config['data_folder'], 'hsb2', config['output'])
