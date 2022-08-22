import os
from dataclasses import dataclass, asdict
from enum import Enum

from dotenv import load_dotenv, set_key, dotenv_values
from snips.config.config import load_prompt_questions

CONFIG_HOME = os.path.join(os.environ['HOME'], '.snips')
CONFIG_PATH = os.path.join(CONFIG_HOME, 'config.env')
THEMES_URI = os.path.join(CONFIG_HOME, 'themes.json')


class ConfigEnum(str, Enum):
    DB_PROVIDER = 'DB_PROVIDER'
    DB_URI = 'DB_URI'
    FORMAT = 'FORMAT'
    HEADER_STYLE = 'HEADER_STYLE'
    SNIPPET_STYLE = 'SNIPPET_STYLE'
    TEXT_STYLE = 'TEXT_STYLE'
    THEME = 'THEME'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


@dataclass
class Configuration:
    DB_PROVIDER: str = 'json'
    DB_URI: str = os.path.join(CONFIG_HOME, 'snips-db.json')
    FORMAT: str = 'table'
    HEADER_STYLE: str = 'yellow'
    SNIPPET_STYLE: str = 'green'
    TEXT_STYLE: str = 'dark_orange'
    THEME: str = 'default'

    @classmethod
    def from_environ(cls):
        init_di = {key: os.environ.get(key) for key in ConfigEnum.list()}
        return cls(**init_di)

    def __post_init__(self):
        di = asdict(self)
        assert set(ConfigEnum.list()) == set(di.keys())

    def dict(self) -> dict:
        return asdict(self)


def init_configuration():
    if not os.path.exists(CONFIG_HOME):
        os.mkdir(CONFIG_HOME)
    if not os.path.exists(CONFIG_PATH):
        for key, value in Configuration().dict().items():
            set_key(CONFIG_PATH, key, value)


def sync_configuration():
    old_config = dotenv_values(CONFIG_PATH)
    current_config = Configuration().dict()
    diff = set(current_config.keys()).difference(old_config.keys())
    if diff:
        for key in diff:
            set_key(CONFIG_PATH, key, current_config[key])


if not os.path.exists(CONFIG_PATH):
    init_configuration()

sync_configuration()
load_dotenv(CONFIG_PATH)

CONFIG = Configuration.from_environ()

PROMPT_QUESTIONS = load_prompt_questions()
