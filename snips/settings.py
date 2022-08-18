import os

from dotenv import load_dotenv
from snips.config.config import load_prompt_questions


load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_PROVIDER = os.environ['DB_PROVIDER']
DB_URI = os.environ['DB_URI']
SNIPPET_TABLE = os.environ['SNIPPET_TABLE']
LOGGER_PROVIDER = os.environ['LOGGER_PROVIDER']
PROMPT_QUESTIONS = load_prompt_questions()
