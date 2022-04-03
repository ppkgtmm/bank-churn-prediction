from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from pandas.core.frame import DataFrame
from utilities import print_evaluation_summary, plot_feature_importance
from constants import seed

algo_map = {
    "Decision Tree": DecisionTreeClassifier,
    "Random Forest": RandomForestClassifier,
    "Logistic Regression": LogisticRegression,
    "SVC": SVC,
}


def model_and_evaluate(X_train, y_train, X_test, y_test, algo):
    model = algo_map.get(algo)

    if model is None:
        return model

    model = model(random_state=seed).fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print_evaluation_summary(y_test, y_pred, algo)

    if hasattr(model, "feature_importances_") and type(X_train) == DataFrame:
        plot_feature_importance(model.feature_importances_, algo, X_train.columns)

    return model
