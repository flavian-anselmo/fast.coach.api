
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_host: str 
    database_password:str
    database_name:str 
    database_username: str 
    algorithm: str 
    secret_key:str

    # africas talking 
    africas_talking_api_key:str 
    africas_talking_env:str
    sender_code:str
    
    

    class Config:
        env_file = ".env"

settings = Settings()