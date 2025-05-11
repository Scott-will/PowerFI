"""Database config."""
from os import path
import os

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)
yahoo_client_id = os.getenv("YAHOO_CONSUMER_KEY")
yahoo_client_secret = os.getenv("YAHOO_CONSUMER_SECRET")
yahoo_redirect_uri = os.getenv("YAHOO_REDIRECT_URI")

CLEANUP_DATA = False