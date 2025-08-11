import joblib, os
from .feature_map import build_feature_matrix

class ModelService:
    def __init__(self, model_path, feature_path, version_file):
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_path)
        self.version = open(version_file).read().strip() if os.path.exists(version_file) else "unknown"

    def predict(self, rows):
        X = build_feature_matrix(rows, self.feature_names)
        y = self.model.predict(X)
        return y.tolist()
