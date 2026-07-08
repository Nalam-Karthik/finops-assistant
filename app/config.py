from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # sqlite:/// (3 slashes) = relative path. Portable across machines.
    database_url: str = "sqlite:///./finops.db"

    # Plain strings, not client objects — this is what makes swapping
    # OpenAI for Ollama later a one-line change instead of a rewrite.
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"

    chroma_persist_dir: str = "./chroma_data"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instantiated once. Every other file does `from app.config import settings`
# and gets this same object.
settings = Settings()