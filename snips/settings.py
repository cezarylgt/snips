import os

from dotenv import load_dotenv

load_dotenv()

DB_URI = os.environ['TINYDB_URI']
SNIPPET_TABLE = os.environ['SNIPPET_TABLE']
NAMESPACE_TABLE = os.environ['NAMESPACE_TABLE']
