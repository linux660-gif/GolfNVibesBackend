from pydantic_settings import BaseSettings, SettingsConfigDict





class EmailSetting(BaseSettings):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str
    mail_port: int
    mail_starttls: bool
    mail_ssl_tls: bool
    use_credentials: bool
    validate_certs: bool
    model_config = SettingsConfigDict(env_file="/home/nusytech/Documents/Software Engineering/Projects/GolfNVibesBackend/.env")



email_setting = EmailSetting() # type: ignore


