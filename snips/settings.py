import os

from dotenv import load_dotenv

load_dotenv()

DB_PROVIDER = os.environ['DB_PROVIDER']
DB_URI = os.environ['DB_URI']
SNIPPET_TABLE = os.environ['SNIPPET_TABLE']
NAMESPACE_TABLE = os.environ['NAMESPACE_TABLE']
LOGGER_PROVIDER = os.environ['LOGGER_PROVIDER']
