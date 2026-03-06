from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    LASTFM_API_KEY: str = ""
    AUDIODB_API_KEY: str = ""
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()