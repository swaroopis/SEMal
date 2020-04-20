from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
import sys
from configkmal import human, mice

if len(sys.argv) <= 1:
    print('Please Specify human or mice')
    exit(1)

config = human if sys.argv[1] == 'human' else mice

PSSM_folder = config['PSSM_folder']
SPD3_folder = config['SPD3_folder']

WINDOW_SIZE = 12
STRUCTURAL_WINDOW_SIZE = 3
LOWEST_VAL = 20

data = {}
final_data = {}


def format_to_normal(protein):
    res = []
    for p in protein:
        if p != "O":
            res.append(p)
    return "".join(res)


def encoded_to_mapping(encoded):
    global data
    data = {}
    proteins = [f for f in listdir(encoded) if isfile(join(encoded, f)) and f.endswith('seq')]
    for protein in proteins:
        with open(encoded + protein, 'r') as fp:
            now_protein = protein[0:-4]
            fp.readline()
            now_seq = fp.readline().strip()
            data[now_protein] = format_to_normal(now_seq)


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


def get_profile_bigram(PSSM, flatten=False):
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


def get_bigrams(protein, seq, site_str, m_or_not):
    X = []
    Y = []
    ind = 0

    while ind < len(seq):
        ind = seq.find(site_str, ind)
        if ind == -1:
            break

        PSSM = get_PSSM(protein, len(seq), ind)
        PSSM_bigram = get_profile_bigram(PSSM, True)  # 20 x 20
        SPpre = get_structural_info(protein, len(seq), ind, True) # 7 x 8
        ind += 1

        combined = np.concatenate((PSSM_bigram, SPpre))

        # print(combined.shape)
        X.append(combined)
        Y.append(int(m_or_not))

    return [X, Y]


def main(data_folder, ext, output):
    global data

    encoded_to_mapping(data_folder)
    # print(data_folder)
    proteins = [f[0:-4] for f in listdir(data_folder) if isfile(join(data_folder, f)) and f.endswith(ext)]

    X_p = []
    Y_p = []
    X_n = []
    Y_n = []
    for protein in tqdm(proteins):
        # For all Positive Sites
        [a, b] = get_bigrams(protein, data[protein], 'K', 1)
        X_p += a
        Y_p += b
        # print(X_p, Y_p)

        # # For all Negative Sites
        # [c, d] = get_bigrams(protein, mathematical_seq, '0')
        # X_n += c
        # Y_n += d

    np.savez('{}'.format(output), X_p, Y_p, X_n, Y_n)


main(config['data_folder'], 'seq', config['output'])
