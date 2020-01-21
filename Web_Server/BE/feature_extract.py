import numpy as np

WINDOW_SIZE = 20
STRUCTURAL_WINDOW_SIZE = 3
LOWEST_VAL = 20

data = {}
final_data = {}


def get_PSSM(protein, protein_sz, ind, PSSMs):
    PSSM_list = []

    PSSMs = PSSMs[1:]
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


def get_structural_info(protein, protein_sz, ind, SSpres):
    SSpre_list = []

    for val in range(ind - STRUCTURAL_WINDOW_SIZE, ind + STRUCTURAL_WINDOW_SIZE + 1):
        now = val
        if val < 0 or val >= protein_sz:
            distance = ind - val
            now = ind + distance

        row = list(map(float, SSpres[now].strip().split()[3:]))
        SSpre_list.append(row)

    return np.asarray(SSpre_list).flatten()


def get_bigrams(protein, seq, site_str, pssm, spd3):
    ind = 0

    X = []
    Y = []
    while ind < len(seq):
        ind = seq.find(site_str, ind)
        if ind == -1:
            break

        PSSM = get_PSSM(protein, len(seq), ind, pssm)
        PSSM_bigram = get_profile_bigram(PSSM, True)  # 20 x 20
        SPpre = get_structural_info(protein, len(seq), ind, spd3)
        ind += 1

        combined = np.concatenate((PSSM_bigram, SPpre))

        X.append(combined)
        Y.append(ind)

    return [X, Y]
