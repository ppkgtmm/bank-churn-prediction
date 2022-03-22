import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .data import get_classes
from .preprocess import label_encode

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


def plot_categorical_features(data: pd.DataFrame, target_col: str = 'attrition_flag'):
    classes = get_classes(data, target_col)
    data_by_class = {cls: data[data[target_col] == cls] for cls in classes}
    
    for cat_feature in data.drop(columns=[target_col]).select_dtypes(include=['object']).columns:
        fig, ax = plt.subplots(1, len(classes), figsize=(12,5))
        
        for idx, cls in enumerate(data_by_class.keys()):
            group = data_by_class[cls].groupby(cat_feature).size()
            group = (group / group.sum()).reset_index()
            label = ' '.join(str(cat_feature).split('_'))
            sns.barplot(x=cat_feature, y=0, data=group, ax=ax[idx])
            ax[idx].set_ylabel('Count')
            ax[idx].set_xlabel(label.capitalize())
            ax[idx].set_title('Distribution of {} among {}'.format(label.lower(), cls), fontsize=14)
            ax[idx].set_xticklabels(ax[idx].get_xticklabels(), rotation=45, ha='center')
        plt.show()


def plot_numeric_features(data: pd.DataFrame, target_col: str = 'attrition_flag'):
    classes = get_classes(data, target_col)
    data_by_class = {cls: data[data[target_col] == cls] for cls in classes}
    
    for cat_feature in data.drop(columns=[target_col]).select_dtypes(exclude=['object']).columns:
        fig, ax = plt.subplots(1, len(classes), figsize=(14,5))
        
        for idx, cls in enumerate(data_by_class.keys()):
            label = ' '.join(str(cat_feature).split('_'))
            sns.histplot(x=cat_feature, data=data_by_class[cls], ax=ax[idx], stat='density', bins=15)
            ax[idx].set_ylabel('Density')
            ax[idx].set_xlabel(label.capitalize())
            ax[idx].set_title('Distribution of {} among {}'.format(label.lower(), cls), fontsize=14)
        plt.show()

def plot_corr_hmap(data: pd.DataFrame, target_col: str):
    data[target_col] = label_encode(data[target_col], get_classes(data, target_col))
    corr = data.corr()
    plt.figure(figsize=(8,6))
    plt.title('Correlation heatmap of variables')
    sns.heatmap(corr)
    plt.show()
