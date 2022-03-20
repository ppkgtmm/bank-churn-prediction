import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns


def read_data(data_path, index_col):
    data = pd.read_csv(data_path, index_col=index_col)
    # convert column names to lower case
    data.columns = list(map(lambda col: col.lower(), data.columns))     # easier to work with
    return data


def select_categorical_features(X, y, cat_cols):
    selected_cat = []
    for col in cat_cols:
        stat, pval, df, _ = chi2_contingency(pd.crosstab(X[col], y))
        print('p-value for feature {}: {}'.format(col, pval))
        if pval < 0.05:
            selected_cat.append(col)
    print('\nselected categorical features:', ', '.join(selected_cat))
    return selected_cat


def plot_feature_importance(feature_importances, algo, columns):
    plt.figure(figsize=(8, 6))
    imp_df = (
        pd.DataFrame({
            'column': columns,
            'importance': feature_importances
        })
        .sort_values('importance', ascending=False)
        .query('abs(importance) > 0')
    )
    sns.barplot(y='column', x='importance', data=imp_df, orient='h', palette='muted')
    plt.title('feature importance for {} model'.format(algo), fontdict={'size': 16})
    plt.show()


def get_classes():
    return ["Existing Customer", "Attrited Customer"]