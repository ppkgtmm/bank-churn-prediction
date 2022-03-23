from scipy.stats import chi2_contingency
import pandas as pd


def select_categorical_features(X, y, cat_cols):
    selected_cat = []
    for col in cat_cols:
        stat, pval, df, _ = chi2_contingency(pd.crosstab(X[col], y))
        print("p-value for feature {}: {}".format(col, pval))
        if pval < 0.05:
            selected_cat.append(col)
    print("\nselected categorical features:", ", ".join(selected_cat))
    return selected_cat
