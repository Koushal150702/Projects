""" This is basically the skeleton of the env variables with default values """
""" The .env file will hold the actual values for these constants like passwords"""
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    """
    This class is the 'Contract' for our application. 
    It defines everything the app NEEDS to know.
    """

# App component
    APP_NAME: str = 'AI knowledge engine'

# Database component
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASS: str 
    DB_NAME: str = 'knowledge_db'

    model_config = SettingsConfigDict(env_file='.env') # Must be an attribute for pydantic to know to access .env as pydantic reads configuration per class not globally

    @property
    def DB_URL(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

settings = Settings()
