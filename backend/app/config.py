from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/example_db"
    
    # Elasticsearch settings
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Application settings
    APP_NAME: str = "Translation Platform"
    DEBUG: bool = True

settings = Settings()