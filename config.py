from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    paypal_client_id: str
    paypal_client_secret: str
    paypal_base_url: str
    mpesa_consumer_key: str
    mpesa_consumer_secret: str
    mpesa_base_url : str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore
