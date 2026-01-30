import os
from dataclasses import dataclass

@dataclass
class Settings:
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "NeoSupport Inc.")
    COMPANY_PHONE: str = os.getenv("COMPANY_PHONE", "+998 71 000 00 00")
    COMPANY_EMAIL: str = os.getenv("COMPANY_EMAIL", "support@neosupport.example")
    COMPANY_WEBSITE: str = os.getenv("COMPANY_WEBSITE", "https://neosupport.example")

    RAW_DATA_DIR: str = os.getenv("RAW_DATA_DIR", "data/raw")
    PROCESSED_DIR: str = os.getenv("PROCESSED_DIR", "data/processed")

    FAISS_INDEX_PATH: str = os.path.join(PROCESSED_DIR, "index.faiss")
    DOCSTORE_PATH: str = os.path.join(PROCESSED_DIR, "docstore.pkl")

    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # Retrieval tuning
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    MIN_SIM_SCORE: float = float(os.getenv("MIN_SIM_SCORE", "0.30"))  # adjust after testing

    # LLM (OpenAI) - for function calling + answers
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # GitHub Issues integration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "")  # e.g. "yourname/yourrepo"

settings = Settings()
