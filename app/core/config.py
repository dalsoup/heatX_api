import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "dev")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/trained_model.pkl")
    FEATURE_PATH: str = os.getenv("FEATURE_PATH", "models/feature_names.pkl")
    MODEL_VERSION_FILE: str = os.getenv("MODEL_VERSION_FILE", "models/VERSION")

settings = Settings()
