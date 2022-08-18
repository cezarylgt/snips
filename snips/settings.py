import os
from enum import Enum

from dotenv import load_dotenv, set_key
from snips.config.config import load_prompt_questions

# CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
CONFIG_HOME = os.path.join(os.environ['HOME'], '.snips')
CONFIG_PATH = os.path.join(CONFIG_HOME, 'config.env')


class Configuration:
    DB_PROVIDER = 'json'
    DB_URI = os.path.join(CONFIG_HOME, 'snips-db.json')
    FORMAT = 'table'


def init_configuration():
    if not os.path.exists(CONFIG_HOME):
        os.mkdir(CONFIG_HOME)
    if not os.path.exists(CONFIG_PATH):
        set_key(CONFIG_PATH, ConfigEnum.FORMAT, Configuration.FORMAT)
        set_key(CONFIG_PATH, ConfigEnum.DB_URI, Configuration.DB_URI)
        set_key(CONFIG_PATH, ConfigEnum.DB_PROVIDER, Configuration.DB_PROVIDER)


class ConfigEnum(str, Enum):
    DB_PROVIDER = 'DB_PROVIDER'
    DB_URI = 'DB_URI'
    FORMAT = 'FORMAT'


if not os.path.exists(CONFIG_PATH):
    init_configuration()

load_dotenv(CONFIG_PATH)

DB_PROVIDER = os.environ['DB_PROVIDER']
DB_URI = os.environ['DB_URI']
SNIPPET_TABLE = os.environ.get('SNIPPET_TABLE', 'Snippets')
FORMAT = os.environ['FORMAT']
PROMPT_QUESTIONS = load_prompt_questions()
