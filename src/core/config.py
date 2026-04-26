from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key:str
    database_url:str
    vector_db_path:str="./data/vector_db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()