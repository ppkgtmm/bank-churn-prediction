import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .data import get_classes
from .preprocess import label_encode

plt_save_config = dict(dpi=200, bbox_inches="tight")


def plot_column_values(ax, values, columns, title):
    plt.figure(figsize=(8, 6))
    df = pd.DataFrame({"column": columns, "value": values})
    df = df.sort_values("value", ascending=False)
    sns.barplot(y="column", x="value", data=df, orient="h", palette="muted", ax=ax)
    plt.title(title)
    plt.show()


def plot_categorical_features(
    data: pd.DataFrame, target_col: str = "attrition_flag", save_path: str = None
):
    classes = get_classes(data, target_col)
    data_by_class = {cls: data[data[target_col] == cls] for cls in classes}

    for cat_feature in (
        data.drop(columns=[target_col]).select_dtypes(include=["object"]).columns
    ):
        fig, ax = plt.subplots(1, len(classes), figsize=(12, 5))

        for idx, cls in enumerate(data_by_class.keys()):
            group = data_by_class[cls].groupby(cat_feature).size()
            group = (group / group.sum()).reset_index()
            label = " ".join(str(cat_feature).split("_"))
            sns.barplot(x=cat_feature, y=0, data=group, ax=ax[idx])
            ax[idx].set_ylabel("Count")
            ax[idx].set_xlabel(label.capitalize())
            ax[idx].set_title(
                "Distribution of {} among {}".format(label.lower(), cls), fontsize=14
            )
            ax[idx].set_xticklabels(ax[idx].get_xticklabels(), rotation=45, ha="center")
        if save_path:
            file_name = "{}_distribution.jpg".format(cat_feature)
            full_save_path = os.path.join(save_path, file_name)
            plt.savefig(full_save_path, **plt_save_config)
            plt.close()
        else:
            plt.show()


def plot_numeric_features(
    data: pd.DataFrame, target_col: str = "attrition_flag", save_path: str = None
):
    classes = get_classes(data, target_col)
    data_by_class = {cls: data[data[target_col] == cls] for cls in classes}

    for num_feature in (
        data.drop(columns=[target_col]).select_dtypes(exclude=["object"]).columns
    ):
        fig, ax = plt.subplots(1, len(classes), figsize=(14, 5))

        for idx, cls in enumerate(data_by_class.keys()):
            label = " ".join(str(num_feature).split("_"))
            sns.histplot(
                x=num_feature,
                data=data_by_class[cls],
                ax=ax[idx],
                stat="density",
                bins=15,
            )
            ax[idx].set_ylabel("Density")
            ax[idx].set_xlabel(label.capitalize())
            ax[idx].set_title(
                "Distribution of {} among {}".format(label.lower(), cls), fontsize=14
            )
        if save_path:
            file_name = "{}_distribution.jpg".format(num_feature)
            full_save_path = os.path.join(save_path, file_name)
            plt.savefig(full_save_path, **plt_save_config)
            plt.close()
        else:
            plt.show()


def plot_corr_hmap(
    data: pd.DataFrame, target_col: str = "attrition_flag", save_path: str = None
):
    data[target_col] = label_encode(data[target_col], get_classes(data, target_col))
    corr = data.corr()
    plt.figure(figsize=(8, 6))
    plt.title("Correlation heatmap of variables")
    sns.heatmap(corr)
    plt.show()
    if save_path:
        full_save_path = os.path.join(save_path, "correlation_heatmap.jpg")
        plt.savefig(full_save_path, **plt_save_config)
        plt.close()
    else:
        plt.show()


def plot_labels(
    data: pd.DataFrame, target_col: str = "attrition_flag", save_path: str = None
):
    flag_cnt = data[target_col].value_counts(normalize=True)
    plt.figure(figsize=(8, 4))
    ax = sns.barplot(y=flag_cnt.index, x=flag_cnt, orient="h")
    ax.bar_label(ax.containers[0], padding=5)
    plt.title("Distribution of attrition flag among customers")
    plt.ylabel("Attrition flag")
    plt.xlabel("Proportion")
    if save_path:
        full_save_path = os.path.join(save_path, "label_distribution.jpg")
        plt.savefig(full_save_path, **plt_save_config)
        plt.close()
    else:
        plt.show()
