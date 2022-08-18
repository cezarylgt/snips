import os
from enum import Enum

from dotenv import load_dotenv
from snips.config.config import load_prompt_questions

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(CONFIG_PATH)

DB_PROVIDER = os.environ['DB_PROVIDER']
DB_URI = os.environ['DB_URI']
SNIPPET_TABLE = os.environ['SNIPPET_TABLE']
CONSOLE_OUTPUT = os.environ['CONSOLE_OUTPUT']
PROMPT_QUESTIONS = load_prompt_questions()


class ConfigEnum(str, Enum):
    DB_PROVIDER = 'DB_PROVIDER'
    DB_URI = 'DB_URI'
    SNIPPET_TABLE = 'SNIPPET_TABLE'
    CONSOLE_OUTPUT = 'CONSOLE_OUTPUT'
    PROMPT_QUESTIONS = 'PROMPT_QUESTIONS'
