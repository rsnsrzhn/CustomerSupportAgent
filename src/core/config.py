from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str
    
    EMAIL_HOST: str 
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_MANAGER: str
    
    IMAP_SERVER: str = "imap.gmail.com"
    VECTOR_DB_PATH: str = "./data/vector_db"

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        env_file_encoding="utf-8"
    )

settings = Settings()