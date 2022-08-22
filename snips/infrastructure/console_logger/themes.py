import abc
from dataclasses import dataclass, asdict

from tinydb import TinyDB, Query

from snips.settings import CONFIG
import snips.settings as settings


class Styles:
    header = CONFIG.HEADER_STYLE
    snippet = CONFIG.SNIPPET_STYLE
    text = CONFIG.TEXT_STYLE


@dataclass
class Theme:
    name: str
    header: str
    text: str
    _alias: str = None
    _snippet: str = None
    _desc: str = None
    _tags: str = None
    _defaults: str = None

    @property
    def alias(self):
        return self._alias or self.text

    @property
    def snippet(self):
        return self._snippet or self.text

    @property
    def desc(self):
        return self._desc or self.text

    @property
    def tags(self):
        return self._tags or self.text

    @property
    def defaults(self):
        return self._defaults or self.text

    def dict(self) -> dict:
        return asdict(self)


class ThemeNotFound(Exception):
    pass


DEFAULT_THEME = Theme(
    name='default',
    header='blue',
    text='green',
    _snippet='dark_orange',
    _alias='magenta',
    _desc='yellow'

)


class IThemeRepository:

    @abc.abstractmethod
    def get_by_id(self, id: str): ...


class TinydbThemeRepository(IThemeRepository):

    def __init__(self, path: str = settings.THEMES_URI):
        self.db = TinyDB(path)
        self.table = self.db.table('themes')

        self._query = Query()

    def get_by_id(self, id: str):
        if id == 'default':
            return DEFAULT_THEME

        result = self.table.get(self._query.name == id)
        if result:
            return Theme(**result)
        raise ThemeNotFound


def get_current_theme() -> Theme:
    return TinydbThemeRepository().get_by_id(settings.CONFIG.THEME)
