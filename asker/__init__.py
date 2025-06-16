
from os import getenv

from dotenv import load_dotenv

from .settings import Settings

load_dotenv(getenv("ENV_FILE"))

settings = Settings()
print(settings.database_url)
