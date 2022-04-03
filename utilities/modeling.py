from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from constants import seed

algo_map = {
    "Decision Tree": DecisionTreeClassifier,
    "Random Forest": RandomForestClassifier,
    "Logistic Regression": LogisticRegression,
    "Support Vector Machine": SVC,
}


def do_moedeling(X_train, y_train):
    models = []
    algos = []
    for algo, cls in algo_map.items():
        algos.append(algo)
        model = cls(random_state=seed, class_weight="balanced").fit(X_train, y_train)
        models.append(model)
    return algos, models
