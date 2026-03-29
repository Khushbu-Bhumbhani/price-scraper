import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name:str)->str:
    value=os.getenv(name)
    if not value:
        raise ValueError(f"Missing required env variable: {name}")
    return value

EMAIL_SENDER=get_env_variable("EMAIL_SENDER")
EMAIL_PASSWORD=get_env_variable("EMAIL_PASSWORD")
EMAIL_RECEIVER=get_env_variable("EMAIL_RECEIVER")