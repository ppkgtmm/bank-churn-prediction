import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

# import matplotlib.pyplot as plt
# import seaborn as sns


def get_evaluation_report(models: dict, X_test, y_test):
    df = pd.DataFrame(
        columns=["algorithm", "class", "precision", "recall", "f1", "support"]
    )
    for algo, model in models.items():
        y_pred = model.predict(X_test)
        prec, rec, f1, support = precision_recall_fscore_support(y_test, y_pred)
        for c, (p, r, f, s) in enumerate(zip(prec, rec, f1, support)):
            df.loc[len(df.index)] = [algo, c, p, r, f, s]
    return df


# def plot_confusion_matrix(ax, y_true, y_pred, algo, normalize="true"):
#     conf_mat = pd.DataFrame(confusion_matrix(y_true, y_pred, normalize=normalize))
#     #   plt.figure(figsize=(6, 4))
#     sns.heatmap(conf_mat, annot=True, fmt=".3f", ax=ax)  # plot confusion matrix
#     plt.title("confusion matrix for {} model".format(algo), fontdict={"size": 16})
#     plt.ylabel("true class")
#     plt.xlabel("predicted class")
#     plt.show()


# def print_evaluation_summary(y_true, y_pred, algo):

#     print(classification_report(y_true, y_pred), "\n")

#     plot_confusion_matrix(y_true, y_pred, algo)
