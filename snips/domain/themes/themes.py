import abc
from dataclasses import dataclass, asdict


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


