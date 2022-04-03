from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from constants import seed, dt_algo, rf_algo, lr_algo, svm_algo

algo_map = {
    dt_algo: DecisionTreeClassifier,
    rf_algo: RandomForestClassifier,
    lr_algo: LogisticRegression,
    svm_algo: SVC,
}


def do_modeling(X_train, y_train):
    models = {}
    for algo, cls in algo_map.items():
        model = cls(random_state=seed, class_weight="balanced").fit(X_train, y_train)
        models[algo] = model
    return models
