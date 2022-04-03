import pandas as pd
from sklearn.metrics import precision_recall_fscore_support


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
