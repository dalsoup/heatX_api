import numpy as np

def build_feature_matrix(rows, feature_names):
    X = []
    for i, r in enumerate(rows):
        vec = []
        for f in feature_names:
            if not hasattr(r, f):
                raise ValueError(f"Missing required feature '{f}' at row {i}")
            vec.append(getattr(r, f))
        X.append(vec)
    return np.array(X, dtype=float)
