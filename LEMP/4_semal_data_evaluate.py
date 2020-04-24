from rotation_forest import RotationForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, matthews_corrcoef, precision_score, roc_auc_score
from error_measurement import matthews_correlation, sensitivity, specificity, auc, f1_score
import pickle
import tensorflow as tf
from config import human, mice
import sys


if len(sys.argv) <= 1:
    print('Please Specify human or mice')
    exit(1)

config = human if sys.argv[1] == 'human' else mice


def lemp_compare(x_test, y_test):
    model = pickle.load(open(config['model'], 'rb'))

    y_test_predict = model.predict(x_test)
    print(y_test_predict)

    with tf.Session() as sess:
        sen = sess.run(sensitivity(y_test, y_test_predict))
        spe = sess.run(specificity(y_test, y_test_predict))

    res = "\n******************** Independent Test Score ********************\n"
    res += "Accuracy: {}\n".format(accuracy_score(y_test, y_test_predict))
    res += "MCC: {}\n".format(matthews_corrcoef(y_test, y_test_predict))
    res += "Precision: {}\n".format(precision_score(y_test, y_test_predict))
    res += "Roc AUC score: {}\n".format(roc_auc_score(y_test, y_test_predict))
    res += "AUC score: {}\n".format(auc(y_test, y_test_predict))
    res += "F1 score: {}\n".format(f1_score(y_test, y_test_predict))
    res += "Sensitivity: {}\n".format(sen)
    res += "Specifity: {}\n\n\n".format(spe)
    print(res)
    # i_want_roc(model, x_test, y_test)


def i_want_roc(model, x_test, y_test):
    from sklearn.metrics import roc_curve
    probs = model.predict_proba(x_test)
    probs = probs[:, 1]
    fper, tper, thresholds = roc_curve(y_test, probs)
    plot_roc_curve(fper, tper)


def plot_roc_curve(fper, tper):
    import matplotlib.pyplot as plt
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    npzfile = np.load(config['output_lemp_compare'], allow_pickle=True)
    X_p = npzfile['arr_0']
    Y_p = npzfile['arr_1']
    X_n = npzfile['arr_2']
    Y_n = npzfile['arr_3']

    print(X_p.shape, X_n.shape)

    X = np.concatenate((X_p, X_n)).astype(np.float)
    Y = np.concatenate((Y_p, Y_n)).astype(np.float)

    X = X.reshape(len(X), 456)

    lemp_compare(X, Y)
