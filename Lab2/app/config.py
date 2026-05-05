from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Corpus Manager"
    DATABASE_URL: str = "sqlite:///./corpus.db"
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 50
    
    class Config:
        env_file = ".env"

settings = Settings()