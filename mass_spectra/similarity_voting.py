from gensim.models import Word2Vec
from matchms import Spectrum, calculate_scores
from spec2vec import Spec2Vec


class SimilarityVoting:
    def __init__(self, spec2vec_model_file, intensity_weighting_power=0.5, allowed_missing_percentage=5.0):
        model = Word2Vec.load(spec2vec_model_file)
        self.spec2vec = Spec2Vec(model=model, intensity_weighting_power=intensity_weighting_power,
                                 allowed_missing_percentage=allowed_missing_percentage)

    def fit(self, X, y):
        self.X = [Spectrum(s) for s in X] # List of known spectra
        self.y = y # Matrix of shape (n_known_spectra, n_targets)

    def predict_proba(self, X):
        X = [Spectrum(s) for s in X] # List of unknown spectra

        # Matrix with known spectra as columns and unknown spectra as rows, shape (n_unknown_spectra, n_known_spectra)
        similarities = calculate_scores(X, self.X, self.spec2vec, is_symmetric=False)

        # Matrix with shape (n_unknown_spectra, n_targets)
        y = similarities.dot(self.y)

        # Return probabilities
        return y
    
    def predict(self, X):
        # Calculate probabilities, matrix with shape (n_unknown_spectra, n_targets)
        y = self.predict_proba(X)

        # Return binary predictions
        return (y > 0.5).astype(int)
    
    def get_metadata_routing(self):
        return {"input": "spectrum", "output": "spectrum"}
    
    def get_params(self, deep=True):
        return {"spec2vec_model_file": self.spec2vec.model, "intensity_weighting_power": self.spec2vec.intensity_weighting_power, "allowed_missing_percentage": self.spec2vec.allowed_missing_percentage}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self.spec2vec, parameter, value)
        return self