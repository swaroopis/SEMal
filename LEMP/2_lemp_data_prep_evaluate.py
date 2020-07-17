import numpy as np
from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, matthews_corrcoef, precision_score, roc_auc_score, confusion_matrix, classification_report
from error_measurement import matthews_correlation, sensitivity, specificity, f1_score, precision_m
import tensorflow as tf
import sys
from config import human, mice


if len(sys.argv) <= 1:
    print('Please Specify human or mice')
    exit(1)

config = human if sys.argv[1] == 'human' else mice

data = {}
result = {}


def encoded_to_mapping(encoded):
    global data
    data = {}
    with open(encoded) as fp:
        fp.readline()
        for line in fp:
            row = list(map(str.strip, line.split(',')))
            data[row[1]] = row[2].strip()


def data_lemp_model(X, Y):
    global data
    X = list(set(X))
    count = 0
    res = ""
    for ind in range(len(X)):
        x = X[ind]
        res += f'>{x}\n'
        res += data[x]
        res += '\n'

        count += 1
        if count % 100 == 0:
            with open(f'../data/lemp/{sys.argv[1]}/server/{count // 100}.txt', 'w') as fp:
                fp.write(res)
                res = ""


def original_result_read(encoded):
    global result
    result = {}
    with open(encoded) as fp:
        fp.readline()
        for line in fp:
            row = list(map(str.strip, line.split(',')))
            # print(row)
            protein_id = row[1].strip()
            protein = row[2].strip()
            seq = row[3].strip()

            ind = 0
            while ind < len(protein):
                ind = protein.find("K", ind)
                if ind == -1:
                    break

                if protein_id not in result:
                    result[protein_id] = {}

                result[protein_id][ind] = 1 if seq[ind] == '1' else 0
                ind += 1


y_test = []
y_test_predict = []
TP, TN, FP, FN = 0, 0, 0, 0


def lemp_result_read():
    data_folder = f'../data/lemp/{sys.argv[1]}/result'
    lemp_results = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]
    for f in lemp_results:
        print(f)
        with open(f'{data_folder}/{f}', 'r') as fp:
            fp.readline()
            for line in fp:
                row = line.strip()
                row = [val.strip() for val in row.split()]
                if len(row) > 5:
                    o3 = row.pop()
                    o2 = row.pop()
                    o1 = row.pop()
                    row.append(o1 + " " + o2 + " " + o3)
                protein_id = row[0]
                lysine_ind = int(row[1]) - 1
                pred = 1 if row[-1].startswith('Yes') else 0
                # print(row, protein_id, lysine_ind, pred)
                y_test.append(result[protein_id][lysine_ind])
                y_test_predict.append(pred)

                global TP, TN, FP, FN
                if result[protein_id][lysine_ind] == pred:
                    if pred == 1:
                        TP += 1
                    else:
                        TN += 1
                else:
                    if result[protein_id][lysine_ind] and pred == 0:
                        FN += 1
                    else:
                        FP += 1


def evaluate():
    print(len(y_test), len(y_test_predict))
    with tf.Session() as sess:
        sen = sess.run(sensitivity(y_test, y_test_predict))
        spe = sess.run(specificity(y_test, y_test_predict))

    res = "\n******************** Independent Test Score ********************\n"
    res += "Accuracy: {}\n".format(accuracy_score(y_test, y_test_predict))
    res += "MCC: {}\n".format(matthews_corrcoef(y_test, y_test_predict))
    res += "Precision: {}\n".format(precision_score(y_test, y_test_predict, pos_label=1))
    res += "Roc AUC score: {}\n".format(roc_auc_score(y_test, y_test_predict))
    # res += "AUC score: {}\n".format(auc(y_test, y_test_predict))
    res += "F1 score: {}\n".format(f1_score(y_test, y_test_predict))
    res += "Sensitivity: {}\n".format(sen)
    res += "Specifity: {}\n\n\n".format(spe)
    print(res)

    print(f"TP: {TP}, TN: {TN}, FP: {FP}, FN: {FN}")


def data_prep_for_lemp_server():
    encoded_to_mapping(config['encoded_file'])
    npzfile = np.load(config['output'], allow_pickle=True)
    X_p = npzfile['arr_0']
    Y_p = npzfile['arr_1']
    X_n = npzfile['arr_2']
    Y_n = npzfile['arr_3']

    print(X_p.shape, X_n.shape)

    x_train_p, x_test_p, y_train_p, y_test_p = train_test_split(X_p, Y_p, test_size=0.1, shuffle=True, random_state=47)
    x_train_n, x_test_n, y_train_n, y_test_n = train_test_split(X_n, Y_n, test_size=0.1, shuffle=True, random_state=47)

    print(x_train_p.shape)
    print(x_train_n.shape)
    print(x_test_p.shape)
    print(x_test_n.shape)

    x_test = np.concatenate((x_test_p, x_test_n))
    y_test = np.concatenate((y_test_p, y_test_n))

    print(x_test.shape, y_test.shape)
    data_lemp_model(x_test, y_test)


def data_evaluate_for_lemp():
    original_result_read(config['encoded_file'])
    lemp_result_read()
    evaluate()


if __name__ == '__main__':
    # data_prep_for_lemp_server()
    data_evaluate_for_lemp()



