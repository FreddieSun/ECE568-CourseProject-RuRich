import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures


class PredictionEngine(object):

    @staticmethod
    def bayes(X: np.ndarray, y: np.ndarray, x: np.ndarray):
        pipe = make_pipeline(
            StandardScaler(),
            PolynomialFeatures(17),
            BayesianRidge(normalize=False)
        )  # type: Pipeline

        pipe.fit(X, y)

        return pipe.predict(x)
