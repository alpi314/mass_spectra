from catboost import CatBoostClassifier, Pool


class CatBoost():
    def __init__(self, iterations):
        self.clf = CatBoostClassifier(
            loss_function='MultiLogloss',
            iterations=iterations,
        )

    def fit(self, X, y):
        self.clf.fit(Pool(X, y))

    def predict(self, X):
        return self.clf.predict(X)
    
    def predict_proba(self, X):
        return self.clf.predict_proba(X)