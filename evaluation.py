import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from utilities import get_classes


def plot_confusion_matrix(y_true, y_pred, algo, classes=get_classes()):
    conf_mat = pd.DataFrame(confusion_matrix(y_true, y_pred, normalize='true'), index=classes, columns=classes)
    plt.figure(figsize=(6, 4))
    sns.heatmap(conf_mat, annot=True, fmt='.3f')    # plot confusion matrix
    plt.title('confusion matrix for {} model'.format(algo), fontdict={'size': 16})
    plt.ylabel('true class')
    plt.xlabel('predicted class')
    plt.show()


def print_evaluation_summary(y_true, y_pred, algo):

    print('Classification report for {} model'.format(algo))
    print(classification_report(y_true, y_pred), '\n')

    plot_confusion_matrix(y_true, y_pred, algo)
